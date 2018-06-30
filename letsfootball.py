import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup


def getStatistics(url):
    absolute_path = '/worldcup/statistics/'
    absolute_url = urljoin(url, absolute_path)

    soup = getRequestAndSoup(absolute_url)

    players = []
    for player in soup.select('div.fi-p__wrapper-text', limit=3):
        for name in player.select('div.fi-p__name'):
            players.append(name.getText().strip())
        for country in player.select('div.fi-p__country'):
            players.append(country.getText().strip())

    title = [i.getText() for i in soup.select('div.fi-statistics-list-4-cols__data > span')]
    values = [i.getText() for i in soup.select('div.fi-statistics-list-4-cols__data > b')]

    players += title[:3] + values[:3]

    print('Top Scorer'.center(80, '-'))
    for i in range(3):
        print(players[2 * i].title(), '|', players[2 * i + 1])
        print(players[i + 6], '-', players[i + 9])
        print('-' * 80)
    else:
        print()
    title = title[3:]
    values = values[3:]

    stats = []
    for t, v in zip(title, values):
        stats.append((t, v))

    print('Overall Stats'.center(80, '-'))
    for i in range(8):
        print(stats[i][0], '-', stats[i][1])
        print('-' * 80)
    else:
        print()

    title = title[12:]
    values = values[12:]

    unknown = [i.getText() for i in soup.select('ul.fi-statistics-list-4-cols > li > div.fi-statistics-list-4-cols__title')]
    unknown = unknown[:4]
    country_name = [i.getText() for i in soup.select('a.fi-t__nText ')]

    print('Team Statistics'.center(80, '-'))
    for i in range(4):
        print(unknown[i], 'by', country_name[i])
        print(title[i].strip(), values[i])
        print('-' * 80)
    else:
        print()


def getGoalsTable(url):
    absolute_path = '/worldcup/statistics/teams/goal-scored'
    absolute_url = urljoin(url, absolute_path)

    soup = getRequestAndSoup(absolute_url)

    headings = []
    for head in soup.findAll('span', {'class': 'th-text-abbr'}):
        headings.append(head.getText().strip())
    headings = ['Rank', 'Team'] + headings

    content = []
    for table in soup.findAll('tr'):
        temp = []
        for data in table.findAll('td'):
            if data:
                temp.append(data.getText().strip())
        content.append(temp)

    del content[0]
    for i in content:
        i[1] = i[1].split('\n')[0]
    content.insert(0, headings)

    print('Goals Scored'.center(80))
    print('=' * 80)
    for i in range(len(content)):
        for j in range(len(content[0])):
            if j == 1:
                print(content[i][j].center(15), end=' |')
            else:
                print(content[i][j].rjust(5), end=' |')
        else:
            print()
        if i == 0:
            print('=' * 80)
        else:
            print('-' * 80)


def getFixtures(url):
    absolute_path = 'worldcup/matches/'
    absolute_url = urljoin(url, absolute_path)

    soup = getRequestAndSoup(absolute_url)
    matches_link = []

    for link in soup.findAll('a', class_='fi-mu__link'):
        matches_link.append(urljoin(url, link.get('href')))

    for match_url in matches_link:
        print('-' * 80)
        soup = getRequestAndSoup(match_url)

        for loc_info in soup.findAll('div', {'class': 'fi__info__location'}):
            for loc in loc_info.select('span'):
                print(loc.getText(), end=' ')
        else:
            print()
        for i in soup.findAll('div', {'class': 'fi-mu__info__datetime'}):
            time = i.getText().strip().split()
            time = time[:5]
            print(" ".join(time))

        playing_teams = []
        for name in soup.findAll('span', {'class': 'fi-t__nText '}):
            playing_teams.append(name.getText())
        playing_teams = playing_teams[:2]

        for sf in soup.findAll('span', {'class': 'fi-t__nTri'}):
            playing_teams.append(sf.getText())

        score = soup.select('span.fi-s__scoreText')[0].getText().strip()

        print(playing_teams[0], playing_teams[2], score, playing_teams[3], playing_teams[1])
    else:
        print('-' * 80)
        return


def getTeamDetails(url, team_url):

    soup = getRequestAndSoup(team_url)

    for a in soup.findAll('div', {'class': 'fi-p'}):
        print('-' * 80)
        if a.find('span', {'class': 'fi-p__num'}):
            print('Jersey No.:', a.find('span', {'class': 'fi-p__num'}).getText())
        else:
            print(':-)')
            break
        for check in a.select('div.fi-p__n a'):
            print('Full name:', check.get('title').title())
            print('Link to profile:', urljoin(url, check.get('href')))
        if a.find('div', {'class': 'fi-p__info--role'}):
            print('Role:', a.find('div', {'class': 'fi-p__info--role'}).getText().strip())
        if a.find('span', {'class': 'fi-p__info--ageNum'}):
            print('Age:', a.find('span', {'class': 'fi-p__info--ageNum'}).getText())

    return


def getTeamsName(url):
    absolute_path = 'worldcup/teams/'
    absolute_url = urljoin(url, absolute_path)
    soup = getRequestAndSoup(absolute_url)

    team_details = []
    team_name = []
    team_links = []

    for team in soup.findAll('a', {'class': 'fi-team-card fi-team-card__team'}):
        team_links.append(urljoin(url, team.get('href')))
    for name in soup.findAll('div', {'class': 'fi-team-card__name'}):
            team_name.append(name.getText().strip())
    for i in range(len(team_links)):
        team_details.append((team_name[i], team_links[i]))

    i = 1
    for team in team_details:
        print('-' * 80)
        print('{}.'.format(i), team)
        i += 1
    else:
        print('~' * 80)
    # Detail has been extarcted. Only print statement is left
    while True:
        per = input('Do you want team details (y/n) ')
        if per == 'y':
            team_no = int(input('Enter the team number to get the details of '))
            getTeamDetails(url, team_links[team_no - 1])
            per = 'n'
        else:
            break

    return


def getRequestAndSoup(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def switcher(choice):
    switch = {
        1: getTeamsName,
        2: getFixtures,
        3: getStatistics,
        4: getGoalsTable
    }
    return switch.get(choice, 'Wrong Choice')


def main():

    url = 'https://www.fifa.com/'

    while True:

        choice = int(input('1. Team Detail\n2. Fixtures\n3. Statistics\n4. Goals table\n:'))
        func = switcher(choice)
        if func == 'Wrong Choice':
            print(func)
            break
        else:
            func(url)


if __name__ == '__main__':
    main()
