package main

import (
	"C"
	"fmt"
	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
	fuzzy "github.com/paul-mannino/go-fuzzywuzzy"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

//export merge
func merge(_sportName *C.char) {

	var sportName string = C.GoString(_sportName)

	startTime := time.Now()
	fmt.Println("... merging scraped data - " + sportName)
	//
	// Load data
	path1 := "C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_import\\maxb_" + sportName + ".txt"
	path2 := "C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_import\\mozz_" + sportName + ".txt"

	df1 := ReadCSVFromFile(path1)
	df2 := ReadCSVFromFile(path2)

	// Order books based by num of records
	var bookie1, bookie2 *dataframe.DataFrame
	var bookieName1, bookieName2 string

	if df1.Nrow() > df2.Nrow() {
		bookie1 = &df1
		bookie2 = &df2
		bookieName1 = getBookieNameFromPath(path1)
		bookieName2 = getBookieNameFromPath(path2)
	} else {
		bookie1 = &df2
		bookie2 = &df1
		bookieName1 = getBookieNameFromPath(path2)
		bookieName2 = getBookieNameFromPath(path1)
	}

	// Merge
	successfulMatches := 0
	recordsToKeep := make([][]string, 0)
	for _, el1 := range bookie1.Maps() {
		mergedRecord := make([]string, 11)
		for _, el2 := range bookie2.Maps() {

			//check if tip_names match
			if el1["tip1_name"] != el2["tip1_name"] || el1["tip2_name"] != el2["tip2_name"] {
				continue
			}

			// check if time match is close
			t1, _ := strconv.ParseInt(el1["kick_off"].(string), 10, 64)
			t2, _ := strconv.ParseInt(el2["kick_off"].(string), 10, 64)
			// 300,000, nznm za ovo vreme ali za sad me ne zajebava
			print(t1, " - ", t2, "\n")
			if t1-600 < t2 || t2 > t1+600 {
				continue
			}

			if sportName == "soccer" {
				if fuzzy.Ratio(el1["1"].(string), el2["1"].(string)) < 80 {
					continue
				}
				if fuzzy.Ratio(el1["2"].(string), el2["2"].(string)) < 80 {
					continue
				}
				mergeRecordsAsIs(&el1, &el2, &mergedRecord)

			} else {

				if fuzzy.Ratio(el1["1"].(string), el2["1"].(string)) >= 80 && fuzzy.Ratio(el1["2"].(string), el2["2"].(string)) >= 80 {
					mergeRecordsAsIs(&el1, &el2, &mergedRecord)

				} else if fuzzy.Ratio(el1["1"].(string), el2["2"].(string)) >= 80 && fuzzy.Ratio(el1["2"].(string), el2["1"].(string)) >= 80 {
					if shouldNotSwitchTipVals(el1["tip1_name"].(string), sportName) {
						mergeRecordsAsIs(&el1, &el2, &mergedRecord)
					} else {
						mergeRecordsSwitched(&el1, &el2, &mergedRecord)
					}

				} else {
					continue
					//// No point in doing this with only 2 bookies because you are just going to remove None rows later
					//if not merged_record:
					//continue
					//// merged_record = [i['1'], i['2'], i['tip1_name'], i['tip1_val'], None, i['tip2_name'], i['tip2_val'], None]
					//
				}
			}
			recordsToKeep = append(recordsToKeep, mergedRecord)
			successfulMatches++
		}
	}

	fmt.Println(bookieName1, ": ", bookie1.Nrow())
	fmt.Println(bookieName2, ": ", bookie2.Nrow())
	fmt.Println("Successfully merged: ", successfulMatches, " records")

	f, err := os.Create("C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_export\\export_" + sportName + ".txt")
	if err != nil {
		log.Fatal(err)
	}

	err = dataframe.LoadRecords(recordsToKeep, dataframe.Names(
		"kick_off",
		"league_"+bookieName1,
		"league_"+bookieName2,
		"1",
		"2",
		"tip1",
		"tip1_"+bookieName1,
		"tip1_"+bookieName2,
		"tip2",
		"tip2_"+bookieName1,
		"tip2_"+bookieName2,
	)).WriteCSV(f)
	if err != nil {
		fmt.Println("ERROR WRITING CSV TO FILE")
		return
	}

	fmt.Println("--- ", time.Now().Sub(startTime), " ---")
}

func getBookieNameFromPath(path string) string {
	bookieName := filepath.Base(path)
	delim := strings.Index(bookieName, "_")
	// if bookieName not in list of bookies throw an error
	return bookieName[0:delim]
}

func ReadCSVFromFile(csvPath string) dataframe.DataFrame {

	file, err := os.Open(csvPath)
	if err != nil {
		log.Fatal(err)
	}

	df := dataframe.ReadCSV(
		file,
		dataframe.HasHeader(true),
		dataframe.DetectTypes(false),
		dataframe.DefaultType(series.String),
	).Arrange(dataframe.Sort("1"))

	err = file.Close()
	if err != nil {
		return dataframe.DataFrame{}
	}

	return df
}

func main() {}

// TODO: Write your own fuzzy matching, where
// - you split by '/' if it's a pair in tennis and then you combine the two scores
// - value partial matching percentage wise, idk just make it better then what you got currently
// - or start a database which you fill with your scraping, and automatically have a que of moz_name - maxb_name y/n

// TODO: parallelize MERGING IN GO

func shouldNotSwitchTipVals(tipName string, sportName string) bool {

	var tipNamesNotToSwitch [4]string
	if sportName == "tennis" {
		tipNamesNotToSwitch = [4]string{"TIE_BREAK_YES", "TIE_BREAK_NO", "TIE_BREAK_FST_SET_YES", "TIE_BREAK_FST_SET_NO"}
	} else {
		return true
	}
	for _, el := range tipNamesNotToSwitch {
		if tipName == el {
			return false
		}
	}
	return true
}

func mergeRecordsAsIs(el1 *map[string]interface{}, el2 *map[string]interface{}, mergedRecord *[]string) {
	(*mergedRecord)[0] = (*el1)["kick_off"].(string)
	(*mergedRecord)[1] = (*el1)["league"].(string)
	(*mergedRecord)[2] = (*el2)["league"].(string)
	(*mergedRecord)[3] = (*el1)["1"].(string)
	(*mergedRecord)[4] = (*el1)["2"].(string)
	(*mergedRecord)[5] = (*el1)["tip1_name"].(string)
	(*mergedRecord)[6] = (*el1)["tip1_val"].(string)
	(*mergedRecord)[7] = (*el2)["tip1_val"].(string)
	(*mergedRecord)[8] = (*el1)["tip2_name"].(string)
	(*mergedRecord)[9] = (*el1)["tip2_val"].(string)
	(*mergedRecord)[10] = (*el2)["tip2_val"].(string)
}

func mergeRecordsSwitched(el1 *map[string]interface{}, el2 *map[string]interface{}, mergedRecord *[]string) {
	(*mergedRecord)[0] = (*el1)["kick_off"].(string)
	(*mergedRecord)[1] = (*el1)["league"].(string)
	(*mergedRecord)[2] = (*el2)["league"].(string)
	(*mergedRecord)[3] = (*el1)["1"].(string)
	(*mergedRecord)[4] = (*el1)["2"].(string)
	(*mergedRecord)[5] = (*el1)["tip1_name"].(string)
	(*mergedRecord)[6] = (*el1)["tip1_val"].(string)
	(*mergedRecord)[7] = (*el2)["tip2_val"].(string)
	(*mergedRecord)[8] = (*el1)["tip2_name"].(string)
	(*mergedRecord)[9] = (*el1)["tip2_val"].(string)
	(*mergedRecord)[10] = (*el2)["tip1_val"].(string)
}
