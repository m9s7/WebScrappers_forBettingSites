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
		mergedRecord := make([]string, 8)
		for _, el2 := range bookie2.Maps() {

			if sportName == "soccer" {
				if el1["tip1_name"] != el2["tip1_name"] || el1["tip2_name"] != el2["tip2_name"] {
					continue
				}
				if fuzzy.Ratio(el1["1"].(string), el2["1"].(string)) < 80 {
					continue
				}
				if fuzzy.Ratio(el1["2"].(string), el2["2"].(string)) < 80 {
					continue
				}
				mergedRecord[0] = el1["1"].(string)
				mergedRecord[1] = el1["2"].(string)
				mergedRecord[2] = el1["tip1_name"].(string)
				mergedRecord[3] = el1["tip1_val"].(string)
				mergedRecord[4] = el2["tip1_val"].(string)
				mergedRecord[5] = el1["tip2_name"].(string)
				mergedRecord[6] = el1["tip2_val"].(string)
				mergedRecord[7] = el2["tip2_val"].(string)
			} else {
				if fuzzy.Ratio(el1["1"].(string), el2["1"].(string)) >= 80 && fuzzy.Ratio(el1["2"].(string), el2["2"].(string)) >= 80 {
					// merge as is
					mergedRecord[0] = el1["1"].(string)
					mergedRecord[1] = el1["2"].(string)
					mergedRecord[2] = el1["tip1_name"].(string)
					mergedRecord[3] = el1["tip1_val"].(string)
					mergedRecord[4] = el2["tip1_val"].(string)
					mergedRecord[5] = el1["tip2_name"].(string)
					mergedRecord[6] = el1["tip2_val"].(string)
					mergedRecord[7] = el2["tip2_val"].(string)
				} else if fuzzy.Ratio(el1["1"].(string), el2["2"].(string)) >= 80 && fuzzy.Ratio(el1["2"].(string), el2["1"].(string)) >= 80 {
					// switch bookie2 record order
					mergedRecord[0] = el1["1"].(string)
					mergedRecord[1] = el1["2"].(string)
					mergedRecord[2] = el1["tip1_name"].(string)
					mergedRecord[3] = el1["tip1_val"].(string)
					mergedRecord[4] = el2["tip2_val"].(string)
					mergedRecord[5] = el1["tip2_name"].(string)
					mergedRecord[6] = el1["tip2_val"].(string)
					mergedRecord[7] = el2["tip1_val"].(string)
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
// TODO: send emails if you find anything
