import requests
from bs4 import BeautifulSoup
from itertools import cycle
import math

proxyCounter = 0
ext = []
teamNames = []
greatestDiff = []
thPointPer = []

def convertNum(stng):
    s = ''

    if len(stng) > 20:
        return 0

    for x in range(len(stng)):
        if x != len(stng) - 1 and stng[x] == '-' and stng[x + 1] != '-':
            s += stng[x]
        
        elif stng[x] == '.':
            s += stng[x]

        elif x != len(stng) - 1 and stng[x] != ',' and stng[x] != "'" and stng[x] != '"' and (not stng[x].isalpha()) and stng[x] != ':' and stng[x].isdigit() and stng[x + 1] != '"':
            s += stng[x]

    if len(s) > 0 and len(s) < 10:
        try:
            return float(s)
        except:
            return 0

    return 0

def convertNum2(stng):
    s = ''

    for x in range(len(stng)):
        if stng[x].isdigit():
            s += stng[x]

    return float(s)


def bubbleSort(subList): 
    
    l = len(subList) 

    for i in range(0, l): 
        
        for j in range(0, l-i-1): 
            
            if (subList[j][0] < subList[j + 1][0]): 
                tempo = subList[j] 
                subList[j]= subList[j + 1] 
                subList[j + 1] = tempo 

    return subList   


def getProxies(inURL):
    page = requests.get(inURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    terms = soup.find_all('tr')
    IPs = []

    for x in range(len(terms)):  
        
        term = str(terms[x])        
        
        if '<tr><td>' in str(terms[x]):
            pos1 = term.find('d>') + 2
            pos2 = term.find('</td>')

            pos3 = term.find('</td><td>') + 9
            pos4 = term.find('</td><td>US<')
            
            IP = term[pos1:pos2]
            port = term[pos3:pos4]
            
            if '.' in IP and len(port) < 6:
                IPs.append(IP + ":" + port)
                #print(IP + ":" + port)

    return IPs 


proxyURL = "https://www.us-proxy.org/"
pxs = getProxies(proxyURL)
proxyPool = cycle(pxs)


def getTeams():
    global ext
    global teamNames
    
    page = requests.get('https://www.landofbasketball.com/nba_teams_year_by_year.htm')
    soup = str(BeautifulSoup(page.text, 'html.parser'))
    
    rawText = soup[soup.find('teams/records_atlanta_hawks.htm') : soup.find('Washington Wizards</a>') + 30]
    raw = rawText

    y = 0
    
    for x in range(30):
        teamNames.append(raw[raw.find('>') + 1: raw.find('<')])
        ext.append(raw[y : raw.find('>') - 1])
        raw = raw[raw.find('<a href') + 9 : ]
    
    #print(teamNames)
    #print(ext)


def getStats():
    global greatestDiff
    getTeams()

    for x in range(len(ext)):
        page = requests.get('https://www.landofbasketball.com/' + ext[x])
        soup = BeautifulSoup(page.text, 'html.parser')
        wl = soup.find_all('tr', {'class': 'top'})
        wins = []
        years = []

        for text in wl:
            line = str(text)
            rawWL = line[line.find('/results_by_team') + 1 : line.find('/results_by_team') + 50]
            wL = float(rawWL[rawWL.find('>') + 1: rawWL.find('-')])
            wins.append(wL)
            years.append(rawWL[rawWL.find('team') + 5 : rawWL.find('team') + 9])
        
        #print(teamNames[x])
        
        #for num in wins:
            #print(num)

        for y in range(len(wins) - 1):
            greatestDiff.append([abs(wins[y] - wins[y + 1]), teamNames[x], years[y]])

        #print('\n\n\n')

    sortedList = bubbleSort(greatestDiff)
    print(sortedList[0 : 10])


def getTeamStats():

    teamAvgs = []
    teamAvgs2 = []
    ratingsAnalysis = []
    ratingsAnalysis2 = []

    teamRankings = [('Milwaukee Bucks', 'MIL', 60), ('Toronto Raptors', 'TOR', 58), ('Golden State Warriors', 'GSW', 57), ('Denver Nuggets', 'DEN', 54),
    ('Portland Trail Blazers', 'POR', 53), ('Houston Rockets', 'HOU', 53), ('Philadelphia 76ers', 'PHI', 51), ('Utah Jazz', 'UTA', 50), ('Oklahoma City Thunder', 'OKC', 49),
    ('Boston Celtics', 'BOS', 49), ('San Antonio Spurs', 'SAS', 48), ('Los Angeles Clippers', 'LAC', 48), ('Indiana Pacers', 'IND', 48), ('Brooklyn Nets', 'BRK', 42), 
    ('Orlando Magic', 'ORL', 42), ('Detroit Pistons', 'DET', 41), ('Sacramento Kings', 'SAC', 39), ('Charlotte Hornets', 'CHO', 39), ('Miami Heat', 'MIA', 39),
    ('Los Angeles Lakers', 'LAL', 37), ('Minnesota Timberwolves', 'MIN', 36), ('Memphis Grizzlies', 'MEM', 33), ('New Orleans Pelicans', 'NOP', 33), ('Dallas Mavericks', 'DAL', 33),
    ('Washington Wizards', 'WAS', 32), ('Atlanta Hawks', 'ATL', 29), ('Chicago Bulls', 'CHI', 22), ('Cleveland Cavaliers', 'CLE', 19), ('Phoenix Suns', 'PHO', 19), 
    ('New York Knicks', 'NYK', 17)]


    for x in range(len(teamRankings)):
        
        page = requests.get('https://www.basketball-reference.com/teams/' + teamRankings[x][1] + '/2019.html', proxies = {"http": next(proxyPool)})
        soup = str(BeautifulSoup(page.text, 'html.parser'))

        #Team Name 
        rawTN = soup[soup.find('<meta content="2018-19,') + 15 : soup.find('<meta content="2018-19,') + 60]
        teName = rawTN[rawTN.find(',') + 1: rawTN.find('roster') - 2].strip()
        #print('Team Name', teName) 

        #FG%
        rawFgPCT = soup[soup.find('data-stat="fg_pct" >') + 18 : soup.find('data-stat="fg_pct" >') + 25]
        fgPCT = float(rawFgPCT[rawFgPCT.find('>') + 1 : rawFgPCT.find('<')])   
        #print('FG%', fgPCT)

        #3P%
        raw3PCT = soup[soup.find('data-stat="fg3_pct" >') + 16 : soup.find('data-stat="fg3_pct" >') + 27]
        fg3PCT = float(raw3PCT[raw3PCT.find('>') + 1 : raw3PCT.find('<')])   
        #print('3P%', fg3PCT)

        #FT%
        rawFTPCT = soup[soup.find('data-stat="ft_pct" >') + 16 : soup.find('data-stat="ft_pct" >') + 27]
        ftPCT = float(rawFTPCT[rawFTPCT.find('>') + 1 : rawFTPCT.find('<')])
        #print('FT%', ftPCT)

        #Offensive Rebounds / Game
        rawORB = soup[soup.find('data-stat="orb_per_g" >') + 10 : soup.find('data-stat="orb_per_g" >') + 30]
        orbPerGame = float(rawORB[rawORB.find('>') + 1 : rawORB.find('<')])
        #print('Offensive Rebounds / Game', orbPerGame)

        #Defensive Rebounds / Game
        rawDRB = soup[soup.find('data-stat="drb_per_g" >') + 10 : soup.find('data-stat="drb_per_g" >') + 30]
        drbPerGame = float(rawDRB[rawDRB.find('>') + 1 : rawDRB.find('<')])
        #print('Defensive Rebounds / Game', drbPerGame)

        #Assists / Game
        rawAstPG = soup[soup.find('data-stat="ast_per_g" >') + 15 : soup.find('data-stat="ast_per_g" >') + 30]
        astPerGame = float(rawAstPG[rawAstPG.find('>') + 1 : rawAstPG.find('<')])
        #print('Assists / Game', astPerGame)

        #Steals / Game
        rawStl = soup[soup.find('data-stat="stl_per_g" >') + 15 : soup.find('data-stat="stl_per_g" >') + 30]
        stlPerGame = float(rawStl[rawStl.find('>') + 1 : rawStl.find('<')])
        #print('Steals / Game', stlPerGame)

        #Blocks / Game
        rawBlk = soup[soup.find('data-stat="blk_per_g" >') + 15 : soup.find('data-stat="blk_per_g" >') + 30]
        blkPerGame = float(rawBlk[rawBlk.find('>') + 1 : rawBlk.find('<')])
        #print('Blocks / Game', blkPerGame)

        #Turnovers / Game
        rawTO = soup[soup.find('data-stat="tov_per_g" >') + 15 : soup.find('data-stat="tov_per_g" >') + 30]
        toPerGame = float(rawTO[rawTO.find('>') + 1 : rawTO.find('<')])
        #print('Turnovers / Game', toPerGame)

        #Fouls / Game
        rawF = soup[soup.find('data-stat="pf_per_g" >') + 15 : soup.find('data-stat="pf_per_g" >') + 30]
        foulsPerGame = float(rawF[rawF.find('>') + 1 : rawF.find('<')])
        #print('Fouls / Game', foulsPerGame)

        #Points / Game
        rawPts = soup[soup.find('data-stat="pts_per_g" >') + 15 : soup.find('data-stat="pts_per_g" >') + 30]
        ptsPerGame = float(rawPts[rawPts.find('>') + 1 : rawPts.find('<')])
        #print('Points / Game', ptsPerGame)

        #11
        fgPCT = 100 * fgPCT
        fg3PCT = 170 * fg3PCT
        ftPCT = 100 * ftPCT
        toPerGame = 5 * toPerGame

        offRating = convertNum(soup[soup.find('data-stat="off_rtg" >') + 21 : soup.find('data-stat="off_rtg" >') + 26])
        defRating = convertNum(soup[soup.find('data-stat="def_rtg" >') + 21 : soup.find('data-stat="def_rtg" >') + 26])

        pAvg = (fgPCT + fg3PCT + ftPCT + orbPerGame + drbPerGame + astPerGame + stlPerGame + blkPerGame - toPerGame - foulsPerGame + ptsPerGame) / 2
        teamAvgs.append([pAvg, teName])
        teamAvgs2.append([pAvg, teName, teamRankings[x][2]])
        ratingsAnalysis.append([defRating, teName, teamRankings[x][2]])
        ratingsAnalysis2.append([offRating, teName, teamRankings[x][2]])


    sortedList = bubbleSort(teamAvgs)
    sortedDefList = bubbleSort(ratingsAnalysis)
    sortedDefList.reverse()
    sortedOffList = bubbleSort(ratingsAnalysis2)

    print()

    '''
    for x in range(len(sortedList)):
        print(sortedList[x][1])

    for x in range(len(sortedList)):
        print(sortedList[x][0])
    '''

    '''
    for x in range(len(teamAvgs2)):
        print(teamAvgs2[x][0])

    for x in range(len(teamAvgs2)):
        print(teamAvgs2[x][1])

    for x in range(len(teamAvgs2)):
        print(teamAvgs2[x][2])
    '''

    '''
    for x in range(len(sortedDefList)):
        print(sortedDefList[x][1])

    for x in range(len(sortedDefList)):
        print(sortedDefList[x][0])

    for x in range(len(sortedDefList)):
        print(sortedDefList[x][2])
    '''

    for x in range(len(sortedOffList)):
        print(sortedOffList[x][1])

    for x in range(len(sortedOffList)):
        print(sortedOffList[x][0])

    for x in range(len(sortedOffList)):
        print(sortedOffList[x][2])

    
def getTeamRankings():
    
    teamSym = ['MIL', 'TOR', 'PHI', 'BOS', 'IND', 'BRK', 'ORL', 'DET', 'CHO', 'MIA', 'WAS', 'ATL', 'CHI', 'CLE',
    'NYK', 'GSW', 'DEN', 'POR', 'HOU', 'UTA', 'OKC', 'SAS', 'LAC', 'SAC', 'LAL', 'MIN', 'MEM', 'NOP', 'DAL', 'PHO']
    
    teamRankings = [('Milwaukee Bucks', 'MIL', 60), ('Toronto Raptors', 'TOR', 58), ('Golden State Warriors', 'GSW', 57), ('Denver Nuggets', 'DEN', 54),
    ('Portland Trail Blazers', 'POR', 53), ('Houston Rockets', 'HOU', 53), ('Philadelphia 76ers', 'PHI', 51), ('Utah Jazz', 'UTA', 50), ('Oklahoma City Thunder', 'OKC', 49),
    ('Boston Celtics', 'BOS', 49), ('San Antonio Spurs', 'SAS', 48), ('Los Angeles Clippers', 'LAC', 48), ('Indiana Pacers', 'IND', 48), ('Brooklyn Nets', 'BRK', 42), 
    ('Orlando Magic', 'ORL', 42), ('Detroit Pistons', 'DET', 41), ('Sacramento Kings', 'SAC', 39), ('Charlotte Hornets', 'CHO', 39), ('Miami Heat', 'MIA', 39),
    ('Los Angeles Lakers', 'LAL', 37), ('Minnesota Timberwolves', 'MIN', 36), ('Memphis Grizzlies', 'MEM', 33), ('New Orleans Pelicans', 'NOP', 33), ('Dallas Mavericks', 'DAL', 33),
    ('Washington Wizards', 'WAS', 32), ('Atlanta Hawks', 'ATL', 29), ('Chicago Bulls', 'CHI', 22), ('Cleveland Cavaliers', 'CLE', 19), ('Phoenix Suns', 'PHO', 19), 
    ('New York Knicks', 'NYK', 17)]

    for x in range(len(teamRankings)):
        
        page = requests.get('https://www.basketball-reference.com/teams/' + teamRankings[x][1] + '/2019.html', proxies = {"http": next(proxyPool)})
        soup = str(BeautifulSoup(page.text, 'html.parser'))

        print(teamRankings[x][0])


def getPlayerStats():
    
    page = requests.get('https://www.basketball-reference.com/leagues/NBA_2020_per_game.html')
    soup = BeautifulSoup(page.text, 'html.parser')
    stats = soup.find_all('tr', {'class': 'full_table'})
    
    playerStats = []

    for text in stats:
        
        line = str(text)

        #print(line)

        name = line[line.find('.html">') + 7 : line.find('</a></td><td class="center')]
        pointsPerGame = convertNum(line[line.find('pts_per_g">') + 11 : line.find('</td></tr>')])
        reboundsPerGame = convertNum(line[line.find('trb_per_g">') + 11 : line.find('trb_per_g">') + 15])
        assistsPerGame = convertNum(line[line.find('ast_per_g">') + 11 : line.find('ast_per_g">') + 15])
        blocksPerGame = convertNum(line[line.find('blk_per_g">') + 11 : line.find('blk_per_g">') + 15])
        stealsPerGame = convertNum(line[line.find('stl_per_g">') + 11 : line.find('stl_per_g">') + 15])
        tovPerGame = convertNum(line[line.find('tov_per_g">') + 11 : line.find('tov_per_g">') + 15])
        foulsPerGame = convertNum(line[line.find('pf_per_g">') + 10 : line.find('pf_per_g">') + 14])
        fgPercentage = convertNum(line[line.find('fg_pct">') + 8 : line.find('fg_pct">') + 13])
        threePointPercentage = convertNum(line[line.find('fg3_pct">') + 9 : line.find('fg3_pct">') + 14])
        efgPercentage = convertNum(line[line.find('efg_pct">') + 9 : line.find('efg_pct">') + 14])
        freeThrowPercentage = convertNum(line[line.find('ft_pct">') + 8 : line.find('ft_pct">') + 13])

        pAvg = pointsPerGame + reboundsPerGame + assistsPerGame + blocksPerGame + stealsPerGame - tovPerGame - foulsPerGame + fgPercentage + threePointPercentage + efgPercentage + freeThrowPercentage

        '''
        print('\n' + name)
        print('Points', pointsPerGame)
        print('Rebounds', reboundsPerGame)
        print('Assists', assistsPerGame)
        print('Blocks', blocksPerGame)
        print('Steals', stealsPerGame)
        print('TOV', tovPerGame)
        print('PF', foulsPerGame)
        print('FG%', fgPercentage)
        print('3P%', threePointPercentage)
        print('EFG%', efgPercentage)
        print('FT%', freeThrowPercentage)
        print('AVG', pAvg)
        print()
        '''

        playerStats.append([name, pAvg, pointsPerGame, reboundsPerGame, assistsPerGame, blocksPerGame, stealsPerGame, tovPerGame, foulsPerGame, fgPercentage, threePointPercentage, efgPercentage, freeThrowPercentage])


    sortedArr = bubbleSort(playerStats)
    
    for x in range(len(sortedArr)):
        print(sortedArr[x][0])
        print('AVG', sortedArr[x][1])
        print('Points', sortedArr[x][2])
        print('Rebounds', sortedArr[x][3])
        print('Assists', sortedArr[x][4])
        print('Blocks', sortedArr[x][5])
        print('Steals', sortedArr[x][6])
        print('TOV', sortedArr[x][7])
        print('PF', sortedArr[x][8])
        print('FG%', sortedArr[x][9])
        print('3P%', sortedArr[x][10])
        print('EFG%', sortedArr[x][11])
        print('FT%', sortedArr[x][12])
        print()


def getBenchStats():

    teamRankings = [('Milwaukee Bucks', 'MIL', 60), ('Toronto Raptors', 'TOR', 58), ('Golden State Warriors', 'GSW', 57), ('Denver Nuggets', 'DEN', 54),
    ('Portland Trail Blazers', 'POR', 53), ('Houston Rockets', 'HOU', 53), ('Philadelphia 76ers', 'PHI', 51), ('Utah Jazz', 'UTA', 50), ('Oklahoma City Thunder', 'OKC', 49),
    ('Boston Celtics', 'BOS', 49), ('San Antonio Spurs', 'SAS', 48), ('Los Angeles Clippers', 'LAC', 48), ('Indiana Pacers', 'IND', 48), ('Brooklyn Nets', 'BRK', 42), 
    ('Orlando Magic', 'ORL', 42), ('Detroit Pistons', 'DET', 41), ('Sacramento Kings', 'SAC', 39), ('Charlotte Hornets', 'CHO', 39), ('Miami Heat', 'MIA', 39),
    ('Los Angeles Lakers', 'LAL', 37), ('Minnesota Timberwolves', 'MIN', 36), ('Memphis Grizzlies', 'MEM', 33), ('New Orleans Pelicans', 'NOP', 33), ('Dallas Mavericks', 'DAL', 33),
    ('Washington Wizards', 'WAS', 32), ('Atlanta Hawks', 'ATL', 29), ('Chicago Bulls', 'CHI', 22), ('Cleveland Cavaliers', 'CLE', 19), ('Phoenix Suns', 'PHO', 19), 
    ('New York Knicks', 'NYK', 17)]


    benchPerf = []

    for x in range(len(teamRankings)):
        
        page = requests.get('https://www.basketball-reference.com/teams/' + teamRankings[x][1] + '/2019.html', proxies = {"http": next(proxyPool)})
        soup = str(BeautifulSoup(page.text, 'html.parser'))

        benchPts = 0

        '''
        start = 6

        for y in range(20):
            
            try:
                benchPlayer = soup[soup.find('data-stat="ranker" csk="' + str(start) + '"') : soup.find('data-stat="ranker" csk="' + str(start + 1) + '"')]
                name = benchPlayer[benchPlayer.find('data-stat="player" csk="') + 24 : benchPlayer.find('" ><a href="/players')]
                ppg = convertNum(benchPlayer[benchPlayer.find('pts_per_g') + 10 : benchPlayer.find('pts_per_g') + 20])

                benchPts += ppg

                start += 1

            except:
                print('err')
                break
        '''

        start = 1

        for y in range(5):
            
            try:
                benchPlayer = soup[soup.find('data-stat="ranker" csk="' + str(start) + '"') : soup.find('data-stat="ranker" csk="' + str(start + 1) + '"')]
                name = benchPlayer[benchPlayer.find('data-stat="player" csk="') + 24 : benchPlayer.find('" ><a href="/players')]
                ppg = convertNum(benchPlayer[benchPlayer.find('pts_per_g') + 10 : benchPlayer.find('pts_per_g') + 20])

                benchPts += ppg

                start += 1

            except:
                print('err')
                break

        #print()
        benchPerf.append([benchPts, teamRankings[x][0], teamRankings[x][2]])


    sortedList = bubbleSort(benchPerf)

    for x in range(len(benchPerf)):
        print(sortedList[x][0])

    for x in range(len(benchPerf)):
        print(sortedList[x][1])

    for x in range(len(benchPerf)):
        print(sortedList[x][2])
    

def getAgeStats():

    teamRankings = [('Milwaukee Bucks', 'MIL', 60), ('Toronto Raptors', 'TOR', 58), ('Golden State Warriors', 'GSW', 57), ('Denver Nuggets', 'DEN', 54),
    ('Portland Trail Blazers', 'POR', 53), ('Houston Rockets', 'HOU', 53), ('Philadelphia 76ers', 'PHI', 51), ('Utah Jazz', 'UTA', 50), ('Oklahoma City Thunder', 'OKC', 49),
    ('Boston Celtics', 'BOS', 49), ('San Antonio Spurs', 'SAS', 48), ('Los Angeles Clippers', 'LAC', 48), ('Indiana Pacers', 'IND', 48), ('Brooklyn Nets', 'BRK', 42), 
    ('Orlando Magic', 'ORL', 42), ('Detroit Pistons', 'DET', 41), ('Sacramento Kings', 'SAC', 39), ('Charlotte Hornets', 'CHO', 39), ('Miami Heat', 'MIA', 39),
    ('Los Angeles Lakers', 'LAL', 37), ('Minnesota Timberwolves', 'MIN', 36), ('Memphis Grizzlies', 'MEM', 33), ('New Orleans Pelicans', 'NOP', 33), ('Dallas Mavericks', 'DAL', 33),
    ('Washington Wizards', 'WAS', 32), ('Atlanta Hawks', 'ATL', 29), ('Chicago Bulls', 'CHI', 22), ('Cleveland Cavaliers', 'CLE', 19), ('Phoenix Suns', 'PHO', 19), 
    ('New York Knicks', 'NYK', 17)]


    avgAges = []


    for x in range(len(teamRankings)):
        
        page = requests.get('https://www.basketball-reference.com/teams/' + teamRankings[x][1] + '/2019.html', proxies = {"http": next(proxyPool)})
        soup = str(BeautifulSoup(page.text, 'html.parser'))

        numPlayers = 0
        playerAges = 0

        for y in range(1, 26):
        
            try:
                player = soup[soup.find('data-stat="ranker" csk="' + str(y) + '"') : soup.find('data-stat="ranker" csk="' + str(y + 1) + '"')]
                name = player[player.find('data-stat="player" csk="') + 24 : player.find('" ><a href="/players')]
                age = convertNum(player[player.find('data-stat="age" >') + 17 : player.find('data-stat="age" >') + 20])

                if age == 0:
                    break

                #print(name, age)
                #print()

                numPlayers += 1
                playerAges += age

            except:
                print('err')
                break


        averageAge = playerAges / numPlayers
        avgAges.append([averageAge, teamRankings[x][0], teamRankings[x][2]])

    sortedList = bubbleSort(avgAges)

    for x in range(len(avgAges)):
        print(sortedList[x][0])

    for x in range(len(avgAges)):
        print(sortedList[x][1])

    for x in range(len(avgAges)):
        print(sortedList[x][2])
    

teamWinsByYear = []


def getTeamStatsByYear(year):

    global teamWinsByYear
        
    page = requests.get('https://www.espn.com/nba/standings/_/season/' + str(year) + '/group/league', proxies = {"http": next(proxyPool)})
    soup = str(BeautifulSoup(page.text, 'html.parser'))

    for x in range(30):
        rawTeamName = soup[soup.find('data-idx="' + str(x) + '">') + 200 : soup.find('data-idx="' + str(x) + '">') + 500]
        teamName = rawTeamName[rawTeamName.find('<img alt=') + 10 : rawTeamName.find('" data-clubhouse-uid')]

        teamSymbol = rawTeamName[rawTeamName.find('/name/') + 6 : rawTeamName.find('/name/') + 9].upper()

        if teamSymbol == 'GS/':
            teamSymbol = 'GSW'

        if teamSymbol == 'NO/':
            teamSymbol = 'NOP'

        if teamSymbol == 'SA/':
            teamSymbol = 'SAS'

        if teamSymbol == 'NY/':
            teamSymbol = 'NYK'

        if teamSymbol == 'BKN':
            teamSymbol = 'BRK'

        if teamSymbol == 'WSH':
            teamSymbol = 'WAS'

        if teamSymbol == 'CHA':
            teamSymbol = 'CHO'

        if teamSymbol == 'PHX':
            teamSymbol = 'PHO'

        rawTeamWins = soup[soup.find('displayName":"' + teamName) : soup.find('displayName":"' + teamName) + 1000]
        
        teamWins = convertNum2(rawTeamWins[rawTeamWins.find('"stats":[') + 13 : rawTeamWins.find('"stats":[') + 17])

        teamWinsByYear.append([teamName, teamSymbol, teamWins])

        #print(teamName, teamWins)
        #print()

    #print(soup)


def getTeamPPG(year):

    getTeamStatsByYear(year)

    global teamWinsByYear
    
    teamRankings = [('Milwaukee Bucks', 'MIL', 60), ('Toronto Raptors', 'TOR', 58), ('Golden State Warriors', 'GSW', 57), ('Denver Nuggets', 'DEN', 54),
    ('Portland Trail Blazers', 'POR', 53), ('Houston Rockets', 'HOU', 53), ('Philadelphia 76ers', 'PHI', 51), ('Utah Jazz', 'UTA', 50), ('Oklahoma City Thunder', 'OKC', 49),
    ('Boston Celtics', 'BOS', 49), ('San Antonio Spurs', 'SAS', 48), ('Los Angeles Clippers', 'LAC', 48), ('Indiana Pacers', 'IND', 48), ('Brooklyn Nets', 'BRK', 42), 
    ('Orlando Magic', 'ORL', 42), ('Detroit Pistons', 'DET', 41), ('Sacramento Kings', 'SAC', 39), ('Charlotte Hornets', 'CHO', 39), ('Miami Heat', 'MIA', 39),
    ('Los Angeles Lakers', 'LAL', 37), ('Minnesota Timberwolves', 'MIN', 36), ('Memphis Grizzlies', 'MEM', 33), ('New Orleans Pelicans', 'NOP', 33), ('Dallas Mavericks', 'DAL', 33),
    ('Washington Wizards', 'WAS', 32), ('Atlanta Hawks', 'ATL', 29), ('Chicago Bulls', 'CHI', 22), ('Cleveland Cavaliers', 'CLE', 19), ('Phoenix Suns', 'PHO', 19), 
    ('New York Knicks', 'NYK', 17)]


    teamStat = []
    winsVsProjWins = []
    teamCombStat = []


    for x in range(len(teamWinsByYear)):
        
        page = requests.get('https://www.basketball-reference.com/teams/' + teamWinsByYear[x][1] + '/' + str(year) + '.html', proxies = {"http": next(proxyPool)})
        soup = str(BeautifulSoup(page.text, 'html.parser'))

        rawTeamStats = soup[soup.find('data-stat="player" >Team</th><td') : soup.find('data-stat="player" >Team</th><td') + 3000]
        
        tmPPG = convertNum(rawTeamStats[rawTeamStats.find('data-stat="pts_per_g" >') + 23 : rawTeamStats.find('data-stat="pts_per_g" >') + 29])
        tmRPG = convertNum(rawTeamStats[rawTeamStats.find('data-stat="trb_per_g" >') + 23 : rawTeamStats.find('data-stat="trb_per_g" >') + 28])
        tmAPG = convertNum(rawTeamStats[rawTeamStats.find('data-stat="ast_per_g" >') + 23 : rawTeamStats.find('data-stat="ast_per_g" >') + 28])
        tmBPG = convertNum('0' + rawTeamStats[rawTeamStats.find('data-stat="blk_per_g" >') + 23 : rawTeamStats.find('data-stat="blk_per_g" >') + 28])
        tmFGP = convertNum('0' + rawTeamStats[rawTeamStats.find('data-stat="fg_pct"') + 20 : rawTeamStats.find('data-stat="fg_pct"') + 25])
        tm3FGP = convertNum('0' + rawTeamStats[rawTeamStats.find('data-stat="fg3_pct"') + 21 : rawTeamStats.find('data-stat="fg3_pct"') + 26])
        tm2FGP = convertNum('0' + rawTeamStats[rawTeamStats.find('data-stat="fg2_pct"') + 21 : rawTeamStats.find('data-stat="fg2_pct"') + 26])

        tmOffRating = convertNum(soup[soup.find('data-stat="off_rtg" >') + 21 : soup.find('data-stat="off_rtg" >') + 27])
        tmDefRating = convertNum(soup[soup.find('data-stat="def_rtg" >') + 21 : soup.find('data-stat="def_rtg" >') + 27])

        tmOppEFG =  convertNum(soup[soup.find('data-stat="opp_efg_pct" >') + 25 : soup.find('data-stat="opp_efg_pct" >') + 31])
        tmEFG =  convertNum(soup[soup.find('data-stat="efg_pct" >') + 21 : soup.find('data-stat="efg_pct" >') + 27])

        benchPts = 0
        start = 6
        starterPts = 0
        start2 = 1

        '''
        for y in range(20):
            
            try:
                benchPlayer = soup[soup.find('data-stat="ranker" csk="' + str(start) + '"') : soup.find('data-stat="ranker" csk="' + str(start + 1) + '"')]
                name = benchPlayer[benchPlayer.find('data-stat="player" csk="') + 24 : benchPlayer.find('" ><a href="/players')]
                ppg = convertNum(benchPlayer[benchPlayer.find('pts_per_g') + 10 : benchPlayer.find('pts_per_g') + 20])

                benchPts += ppg
                start += 1

            except:
                print('err')
                break

        for z in range(5):
            
            try:
                benchPlayer = soup[soup.find('data-stat="ranker" csk="' + str(start2) + '"') : soup.find('data-stat="ranker" csk="' + str(start2 + 1) + '"')]
                name = benchPlayer[benchPlayer.find('data-stat="player" csk="') + 24 : benchPlayer.find('" ><a href="/players')]
                ppg = convertNum(benchPlayer[benchPlayer.find('pts_per_g') + 10 : benchPlayer.find('pts_per_g') + 20])

                starterPts += ppg

                start2 += 1

            except:
                print('err')
                break
        '''

        #0.9786
        #combStat = (tmPPG * 2) + (tmRPG * 2) + (tmAPG * 2) + (tmFGP * 100) + (tm3FGP * 100) + (tm2FGP * 5) + (tmBPG) + (tmOppEFG * 50) + (tmOffRating * 20) - (tmDefRating * 20) - (starterPts * 0.5) - (benchPts * 0.2)

        #0.98205
        #combStat = (math.pow(((tmOffRating * 11) + ((200 - tmDefRating) * 9)), 5) / math.pow((200 - tmOffRating) + tmDefRating, 8.9)) * 9000000
        #projectedWins = combStat * 0.038807

        
        combStat = (math.pow(((tmOffRating * 12) + ((200 - tmDefRating) * 10)), 5) / math.pow((200 - tmOffRating) + tmDefRating, 9)) * 9000000
        teamCombStat.append([combStat, teamWinsByYear[x][2] / combStat])

        #print(teamWinsByYear[x][0], teamWinsByYear[x][2], projectedWins)
        #print(teamWinsByYear[x][0], tmTPG)

        print(teamWinsByYear[x][0], tmOffRating, tmDefRating)

        #teamStat.append([tmPPG, teamWinsByYear[x][0], teamWinsByYear[x][2]])
        #teamStat.append([tmRPG, teamWinsByYear[x][0], teamWinsByYear[x][2]])
        #teamStat.append([tmAPG, teamWinsByYear[x][0], teamWinsByYear[x][2]])
        #teamStat.append([tmFGP, teamWinsByYear[x][0], teamWinsByYear[x][2]])
        #teamStat.append([tm3FGP, teamWinsByYear[x][0], teamWinsByYear[x][2]])
        #teamStat.append([tmBPG, teamWinsByYear[x][0], teamWinsByYear[x][2]])
        
        #teamStat.append([combStat, teamWinsByYear[x][0], teamWinsByYear[x][2], math.floor(projectedWins)])
        #winsVsProjWins.append([teamWinsByYear[x][2], projectedWins])

    
    '''
    summOfRatios = 0

    for x in range(len(teamCombStat)):
        summOfRatios += teamCombStat[x][1]

    numRatio = summOfRatios / len(teamCombStat)

    print('NumRatio:', numRatio)
    print()
    '''

    for x in range(len(teamWinsByYear)):

        calcWins = math.floor(teamCombStat[x][0] * 0.041122809527218813)
        
        print(teamWinsByYear[x][0], teamWinsByYear[x][2], calcWins)
        print()

        teamStat.append([teamCombStat[x][0], teamWinsByYear[x][0], teamWinsByYear[x][2], math.floor(calcWins)])
        winsVsProjWins.append([teamWinsByYear[x][2], calcWins])


    sortedList = bubbleSort(teamStat)

    avgDiff = []

    for x in range(len(winsVsProjWins)):
        avgDiff.append(abs(winsVsProjWins[x][0] - winsVsProjWins[x][1]))

    summ = 0

    for num in avgDiff:
        summ += num

    print()
    print(avgDiff)
    print()
    print(summ / len(avgDiff))


    '''
    print('COMB STATS --------------------------------------------\n\n')

    for x in range(len(teamStat)):
        print(sortedList[x][0])

    print('TEAM NAMES --------------------------------------------\n\n')

    for x in range(len(teamStat)):
        print(sortedList[x][1])

    print('ACTUAL WINS --------------------------------------------\n\n')

    for x in range(len(teamStat)):
        print(sortedList[x][2])

    print('CALCULATED WINS --------------------------------------------\n\n')
    
    for x in range(len(teamStat)):
        print(sortedList[x][3])
    '''
    


#getStats()
#getTeamStats()
#getTeamRankings()
#getPlayerStats()

#getBenchStats()
#getAgeStats()

#getTeamStatsByYear(2018)
#print(teamWinsByYear)
getTeamPPG(2020)
