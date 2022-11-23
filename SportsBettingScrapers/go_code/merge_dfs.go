package main

import (
	"C"
	"errors"
	"fmt"
	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
	fuzzy "github.com/paul-mannino/go-fuzzywuzzy"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"syscall"
	"time"
)

//export merge
func merge(_sportName *C.char) {
	//arg: _sportName * C.char

	var sportName string = C.GoString(_sportName)
	//sportName := "esports"

	startTime := time.Now()
	fmt.Println("... merging scraped data - " + sportName)

	importPaths := []string{
		"C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_import\\maxb_" + sportName + ".txt",
		"C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_import\\mozz_" + sportName + ".txt",
		"C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_import\\soccbet_" + sportName + ".txt",
	}

	var bookies []bookie
	LoadBookiesFromImport(&bookies, &importPaths)
	if len(bookies) < 2 {
		fmt.Println("... nothing to merge - " + sportName)
		for _, b := range bookies {
			fmt.Println(b.name)
		}
		return
	}
	OrderBooksByNumOfRecords(bookies)

	mergedRecords := make([][]string, 0)
	InitMergedRecordsColumns(&mergedRecords, &bookies)
	mergedRecordsColIndxMap := GetColumnIndexes(len(bookies))

	// Merge
	successfulMatches := 0
	for i, el1 := range (*bookies[0].dfPointer).Records() {

		// skip column names row
		if i == 0 {
			continue
		}

		recordToMerge := initRecordWithEl1(&el1, &mergedRecordsColIndxMap, len(bookies))
		doAddRecordToMerged := false

		for bookieOrder := 1; bookieOrder < len(bookies); bookieOrder++ {
			for j, el2 := range (*bookies[bookieOrder].dfPointer).Records() {

				// skip column names row
				if j == 0 {
					continue
				}

				// check if tip_names match
				if el1[tip1Name] != el2[tip1Name] || el1[tip2Name] != el2[tip2Name] {
					continue
				}

				// check if kickoff times are similar
				t1, _ := strconv.ParseInt(el1[kickOff], 10, 64)
				t2, _ := strconv.ParseInt(el2[kickOff], 10, 64)
				oneHour := int64(3600)
				if abs(t1-t2) > oneHour {
					continue
				}

				// check if league numbers match
				if !isSameLeagueNum(el1[league], el2[league]) {
					continue
				}

				if sportName == "soccer" {
					if fuzzy.Ratio(el1[_1_], el2[_1_]) < 80 {
						continue
					}
					if fuzzy.Ratio(el1[_2_], el2[_2_]) < 80 {
						continue
					}

					doAddRecordToMerged = addElToRecord(&el2, bookieOrder, &recordToMerge, &mergedRecordsColIndxMap, false)
					successfulMatches++
					continue
				}

				if fuzzy.Ratio(el1[_1_], el2[_1_]) >= 80 && fuzzy.Ratio(el1[_2_], el2[_2_]) >= 80 {

					doAddRecordToMerged = addElToRecord(&el2, bookieOrder, &recordToMerge, &mergedRecordsColIndxMap, false)
					successfulMatches++
					continue
				}
				if fuzzy.Ratio(el1[_1_], el2[_2_]) >= 80 && fuzzy.Ratio(el1[_2_], el2[_1_]) >= 80 {

					doAddRecordToMerged = addElToRecord(&el2, bookieOrder, &recordToMerge, &mergedRecordsColIndxMap, shouldSwitchTipVals(el1[tip1Name], sportName))
					successfulMatches++
					continue
				}

			}
		}

		if doAddRecordToMerged {
			mergedRecords = append(mergedRecords, recordToMerge)
		}
	}

	for _, bookie := range bookies {
		fmt.Println(bookie.name, ": ", (*bookie.dfPointer).Nrow())
	}
	fmt.Println("Successfully merged: ", successfulMatches, " records")

	f, err := os.Create("C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_export\\export_" + sportName + ".txt")
	if err != nil {
		log.Fatal(err)
	}

	//colsNames = mergedRecordsColIndxMap

	// , dataframe.Names(colsNames...)
	err = dataframe.LoadRecords(mergedRecords).WriteCSV(f)
	if err != nil {
		fmt.Println("ERROR WRITING CSV TO FILE")
		return
	}

	fmt.Println("--- ", time.Now().Sub(startTime), " ---")
}

type bookie struct {
	name      string
	dfPointer *dataframe.DataFrame
}

// Indexes of bookie columns
const (
	kickOff = iota
	league
	_1_
	_2_
	tip1Name
	tip1Val
	tip2Name
	tip2Val
)

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

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

func GetColumnIndexes(numOfBookies int) map[string]int {
	ColIndx := map[string]int{
		"kick_off": 0,
		"league":   1,
	}
	ColIndx["1"] = ColIndx["league"] + numOfBookies
	ColIndx["2"] = ColIndx["1"] + 1
	ColIndx["tip1_name"] = ColIndx["2"] + 1
	ColIndx["tip2_name"] = ColIndx["tip1_name"] + numOfBookies + 1

	return ColIndx
}

func initRecordWithEl1(el1 *[]string, mergedRecordsColIndxMap *map[string]int, numOfBooks int) []string {
	i := mergedRecordsColIndxMap

	mergedRecord := make([]string, 5+3*numOfBooks)

	mergedRecord[(*i)["kick_off"]] = (*el1)[kickOff]
	mergedRecord[(*i)["league"]] = (*el1)[league]
	mergedRecord[(*i)["1"]] = (*el1)[_1_]
	mergedRecord[(*i)["2"]] = (*el1)[_2_]
	mergedRecord[(*i)["tip1_name"]] = (*el1)[tip1Name]
	mergedRecord[(*i)["tip1_name"]+1] = (*el1)[tip1Val]
	mergedRecord[(*i)["tip2_name"]] = (*el1)[tip2Name]
	mergedRecord[(*i)["tip2_name"]+1] = (*el1)[tip2Val]

	// upisi i vred za kvote pa na kraju ako su ostali el svi none samo nemoj da ga ubacis u mergedRecords
	return mergedRecord
}

func addElToRecord(el *[]string, bookieOrder int, record *[]string, mergedRecordsColIndxMap *map[string]int, isSwitched bool) bool {

	i := mergedRecordsColIndxMap

	(*record)[(*i)["league"]+bookieOrder] = (*el)[league]
	if !isSwitched {
		// keep second record as is
		(*record)[(*i)["tip1_name"]+1+bookieOrder] = (*el)[tip1Val]
		(*record)[(*i)["tip2_name"]+1+bookieOrder] = (*el)[tip2Val]
	} else {
		// switch second record
		(*record)[(*i)["tip1_name"]+1+bookieOrder] = (*el)[tip2Val]
		(*record)[(*i)["tip2_name"]+1+bookieOrder] = (*el)[tip1Val]
	}

	return true
}

//TODO: parallelize MERGING IN GO

func LoadBookiesFromImport(bookies *[]bookie, importPaths *[]string) {
	for i := 0; i < len(*importPaths); i++ {

		file, err := os.OpenFile((*importPaths)[i], syscall.O_RDWR, 0755)
		if errors.Is(err, os.ErrNotExist) {
			continue
		}

		df := dataframe.ReadCSV(
			file,
			dataframe.HasHeader(true),
			dataframe.DetectTypes(false),
			dataframe.DefaultType(series.String),
		).Arrange(dataframe.Sort("1"))

		err = file.Truncate(0)
		if err != nil {
			print("File truncate after load failed")
			print(err.Error())
		}
		err = file.Close()
		if err != nil {
			print("File close after load failed")
			print(err.Error())
		}
		if df.Nrow() == 0 {
			continue
		}

		*bookies = append(*bookies, bookie{
			getBookieNameFromPath((*importPaths)[i]),
			&df},
		)
	}
}

func OrderBooksByNumOfRecords(bookies []bookie) {
	sort.Slice(bookies, func(i, j int) bool {
		return (*((bookies[i]).dfPointer)).Nrow() > (*((bookies[j]).dfPointer)).Nrow()
	})
}

func InitMergedRecordsColumns(mergedRecords *[][]string, bookies *[]bookie) {
	colsNames := []string{"kick_off"}
	for _, bookie := range *bookies {
		colsNames = append(colsNames, "league_"+bookie.name)
	}
	colsNames = append(colsNames, "1", "2", "tip1")
	for _, bookie := range *bookies {
		colsNames = append(colsNames, "tip1_"+bookie.name)
	}
	colsNames = append(colsNames, "tip2")
	for _, bookie := range *bookies {
		colsNames = append(colsNames, "tip2_"+bookie.name)
	}

	*mergedRecords = append(*mergedRecords, colsNames)
}

func main() {
	//merge()
}
