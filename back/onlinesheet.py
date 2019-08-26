# -*- coding: utf-8 -*-
import datetime
import os
import os.path
import pickle
import re

import pandas as pd
from googleapiclient.discovery import build


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
TEAM_SHEET = 'Suivi par équipe'
CONVENTION_SHEET = 'Conventions'
ORDER_SHEET = 'Commandes réalisées par équipe'


def breakrange(rangestring):
    coords = rangestring.split('!')[-1]
    return [re.findall('([a-zA-Z]+|[0-9]+)', i) for i in coords.split(':')]


def getrange(sheet, name):
    row_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range='\'' + name + '\'!A:A',
                                valueRenderOption='UNFORMATTED_VALUE').execute()
    row_values = row_result.get('range', [])

    column_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range='\'' + name + '\'!1:1',
                                valueRenderOption='UNFORMATTED_VALUE').execute()
    column_values = column_result.get('range', [])

    if not row_values or not column_values:
        raise ValueError

    row = breakrange(row_values)
    column = breakrange(column_values)
    
    start = row[0]
    end = [column[1][0], row[1][1]]
    fullrange = ':'.join([''.join(i) for i in  [start, end]])

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=name + '!' + fullrange,
                                valueRenderOption='UNFORMATTED_VALUE').execute()
    values = result.get('values', [])
    return values


def aggregateEJ(data):
    df = data[['Numéro de BdC', 'Montant TTC']]
    return df.groupby('Numéro de BdC').sum().reset_index().rename(columns={'index': 'Numéro de BdC'})


def getsheet():
    service = build('sheets', 'v4', developerKey=os.getenv('GOOGLE_API_KEY'))
    return service.spreadsheets()


def getteamdata():
    sheet = getsheet()
    data = getrange(sheet, TEAM_SHEET)
    df = pd.DataFrame(data[1:len(data)], columns=data[0])
    df.ID = df.ID.fillna('')
    return df


def getconventiondata():
    sheet = getsheet()
    data = getrange(sheet, CONVENTION_SHEET)
    df = pd.DataFrame(data[1:len(data)], columns=data[0])
    return df


def getorderdata():
    sheet = getsheet()

    data = getrange(sheet, ORDER_SHEET)
    df = pd.DataFrame(data[1:len(data)], columns=data[0])

    df['Numéro de BdC'] = pd.to_numeric(df['Numéro de BdC'], 'coerce', 'integer').fillna(0)
    df['Montant TTC'] = pd.to_numeric(df['Montant TTC'], 'coerce', 'integer').fillna(0)

    return df


def generateGSAggregate():
    df = getdata()
    agg = aggregateEJ(df)

    now = datetime.datetime.now()
    timestamp = now.isoformat().replace(':','-').replace('.', '-')

    outpath = 'files/gs-' + timestamp + '.csv'
    agg.to_csv(outpath, index=False, decimal=",", sep=";")


def sanitycheck():
    # team = getteamdata()
    # convention = getconventiondata()
    # order = getorderdata()
    # team.to_pickle('onlinesheet.team.pickle')
    # convention.to_pickle('onlinesheet.convention.pickle')
    # order.to_pickle('onlinesheet.order.pickle')

    team = pd.read_pickle('onlinesheet.team.pickle')
    convention = pd.read_pickle('onlinesheet.convention.pickle')
    order = pd.read_pickle('onlinesheet.order.pickle')

    convention_left = convention.merge(team, on='Équipe', how='left', indicator='indicator')
    print(convention_left[convention_left.indicator.str.contains('left_only')])

    keys = ['Équipe', 'Référence convention']
    order_left = order[keys + ['Montant TTC']].groupby(keys).count().reset_index().merge(convention, on=keys, how='left', indicator='indicator')
    print(order_left[order_left.indicator.str.contains('left_only')])

    team.to_json('onlinesheet.team.json', orient="records")
    convention.to_json('onlinesheet.convention.json', orient="records")
    order.to_json('onlinesheet.order.json', orient="records")


def main():
    sanitycheck()


if __name__ == '__main__':
    main()
