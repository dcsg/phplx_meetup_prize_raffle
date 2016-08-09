import urllib.request
import json
import codecs
import jmespath
import random
import ruamel.yaml
from string import Template


def get_prizes() -> list:
    total_prizes = int(input("How many prizes: "))
    prizes = []
    while total_prizes > 0:
        input_prize = input('Add prize: ')
        prizes.append(input_prize)
        total_prizes -= 1

    return prizes


def get_parameters() -> dict:
    parameters = {}
    with open('parameters.yml', 'r') as stream:
        try:
            parameters = ruamel.yaml.load(stream)
        except ruamel.yaml.YAMLError as exc:
            print(exc)

    return parameters


def get_attendees() -> list:
    parameters = get_parameters()
    event_id = input('What\'s the event id?\n')

    endpoint_template = Template('http://api.meetup.com/$urlname/events/$eventid/rsvps?key=$apikey')
    endpoint = endpoint_template.substitute(
        urlname=parameters['url_name'],
        eventid=event_id,
        apikey=parameters['api_key']
    )

    request = urllib.request.Request(endpoint)
    with urllib.request.urlopen(request) as response:
        reader = codecs.getreader("utf-8")
        data = json.load(reader(response))
        attendees = []
        for attendee_name in jmespath.search('[?response != `no`].[member.name]', data):
            attendees.append(attendee_name[0])

        return attendees


def prize_raffle():
    attendees = get_attendees()
    prizes = get_prizes()
    for i in range(0, len(prizes)):
        accept = 'no'
        while accept != 'yes':
            prize = prizes[i]
            winner = attendees.pop(random.randint(0, len(attendees) - 1))
            print('The winner of ' + prize + ' prize is: ' + winner)
            accept = input('accept winner? (yes or no)')


prize_raffle()
