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
	colsNames := []string{
		"kick_off",
		"league_" + bookieName1,
		"league_" + bookieName2,
		"1",
		"2",
		"tip1",
		"tip1_" + bookieName1,
		"tip1_" + bookieName2,
		"tip2",
		"tip2_" + bookieName1,
		"tip2_" + bookieName2,
	}
	mergedRecords := make([][]string, 0)
	mergedRecords = append(mergedRecords, colsNames)
	for _, el1 := range bookie1.Maps() {
		for _, el2 := range bookie2.Maps() {

			//check if tip_names match
			if el1["tip1_name"] != el2["tip1_name"] || el1["tip2_name"] != el2["tip2_name"] {
				continue
			}

			// check if kickoff times are similar
			t1, _ := strconv.ParseInt(el1["kick_off"].(string), 10, 64)
			t2, _ := strconv.ParseInt(el2["kick_off"].(string), 10, 64)
			twentyMinutes := int64(1200)
			if abs(t1-t2) > twentyMinutes {
				continue
			}

			if sportName == "soccer" {
				if fuzzy.Ratio(el1["1"].(string), el2["1"].(string)) < 80 {
					continue
				}
				if fuzzy.Ratio(el1["2"].(string), el2["2"].(string)) < 80 {
					continue
				}
				if !isSameLeagueNum(el1["league"].(string), el2["league"].(string)) {
					continue
				}
				mergeRecords(&el1, &el2, &mergedRecords, false)
				successfulMatches++
				continue

			}

			if fuzzy.Ratio(el1["1"].(string), el2["1"].(string)) >= 80 &&
				fuzzy.Ratio(el1["2"].(string), el2["2"].(string)) >= 80 &&
				isSameLeagueNum(el1["league"].(string), el1["league"].(string)) {

				mergeRecords(&el1, &el2, &mergedRecords, false)
				successfulMatches++
				continue
			}
			if fuzzy.Ratio(el1["1"].(string), el2["2"].(string)) >= 80 &&
				fuzzy.Ratio(el1["2"].(string), el2["1"].(string)) >= 80 &&
				isSameLeagueNum(el1["league"].(string), el1["league"].(string)) {

				mergeRecords(&el1, &el2, &mergedRecords, shouldSwitchTipVals(el1["tip1_name"].(string), sportName))
				successfulMatches++
				continue
			}

			//// No point in doing this with only 2 bookies because you are just going to remove None rows later
			//if not merged_record:
			//continue
			//// merged_record = [i['1'], i['2'], i['tip1_name'], i['tip1_val'], None, i['tip2_name'], i['tip2_val'], None]
			//
		}
	}

	fmt.Println(bookieName1, ": ", bookie1.Nrow())
	fmt.Println(bookieName2, ": ", bookie2.Nrow())
	fmt.Println("Successfully merged: ", successfulMatches, " records")

	f, err := os.Create("C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_export\\export_" + sportName + ".txt")
	if err != nil {
		log.Fatal(err)
	}

	err = dataframe.LoadRecords(mergedRecords, dataframe.Names(colsNames...)).WriteCSV(f)
	if err != nil {
		fmt.Println("ERROR WRITING CSV TO FILE")
		return
	}

	fmt.Println("--- ", time.Now().Sub(startTime), " ---")
}

func main() {}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

//func printSlice(slice []string) {
//	for _, e := range slice {
//		print(e, " ")
//	}
//	print("\n")
//}

func getLeagueNum(league string) int {
	for _, s := range strings.Split(league, " ") {
		leagueNum, err := strconv.Atoi(s)
		if err != nil {
			continue
		}
		return leagueNum
	}
	return -1
}

func isSameLeagueNum(l1 string, l2 string) bool {
	l1LeagueNum := getLeagueNum(l1)
	l2LeagueNum := getLeagueNum(l2)

	if l1LeagueNum >= 2 || l2LeagueNum >= 2 {
		return l1LeagueNum == l2LeagueNum
	}
	return true
}

func getBookieNameFromPath(path string) string {
	bookieName := filepath.Base(path)
	delim := strings.Index(bookieName, "_")
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

func shouldSwitchTipVals(tipName string, sportName string) bool {

	var tipNamesNotToSwitch [4]string
	if sportName == "tennis" {
		tipNamesNotToSwitch = [4]string{"TIE_BREAK_YES", "TIE_BREAK_NO", "TIE_BREAK_FST_SET_YES", "TIE_BREAK_FST_SET_NO"}
	} else {
		return false
	}
	for _, el := range tipNamesNotToSwitch {
		if tipName == el {
			return false
		}
	}
	return true
}

func mergeRecords(el1 *map[string]interface{}, el2 *map[string]interface{}, mergedRecords *[][]string, isSwitched bool) {

	mergedRecord := make([]string, 11)

	//	kick_off,league_maxb,league_mozz,1,2,tip1,tip1_maxb,tip1_mozz,tip2,tip2_maxb,tip2_mozz
	mergedRecord[0] = (*el1)["kick_off"].(string)
	mergedRecord[1] = (*el1)["league"].(string)
	mergedRecord[2] = (*el2)["league"].(string)
	mergedRecord[3] = (*el1)["1"].(string)
	mergedRecord[4] = (*el1)["2"].(string)

	// tip names
	mergedRecord[5] = (*el1)["tip1_name"].(string)
	mergedRecord[8] = (*el1)["tip2_name"].(string)

	// bookie1 tip1 and tip2 values
	mergedRecord[6] = (*el1)["tip1_val"].(string)
	mergedRecord[9] = (*el1)["tip2_val"].(string)

	if !isSwitched {
		// keep second record as is
		mergedRecord[7] = (*el2)["tip1_val"].(string)
		mergedRecord[10] = (*el2)["tip2_val"].(string)
	} else {
		// switch second record
		mergedRecord[7] = (*el2)["tip2_val"].(string)
		mergedRecord[10] = (*el2)["tip1_val"].(string)
	}

	*mergedRecords = append(*mergedRecords, mergedRecord)
}

// TODO: parallelize MERGING IN GO
