# coding=utf-8
#
# listenbrainz-server - Server for the ListenBrainz project
# Copyright (C) 2017 Param Singh
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import listenbrainz.config as config
from listenbrainz import stats


def get_top_recordings(musicbrainz_id, time_interval=None):
    """ Get top recordings of user with given MusicBrainz ID over a particular time interval

        Args:
            musicbrainz_id (str): The MusicBrainz ID of the user
            time_interval  (str): Interval in the BigQuery interval format
                                  which can be seen here:
                                  https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#timestamp_sub

        Returns:
            sorted list of the following format
            [
                {
                    'track_name' (str)
                    'recording_msid' (uuid)
                    'recording_mbid' (uuid)
                    'artist_name' (str)
                    'artist_msid' (uuid)
                    'artist_mbids' (string of comma-seperated uuids)
                    'listen_count' (int)
                }
            ]
    """

    filter_clause = ""
    if time_interval:
        filter_clause = "AND listened_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {})".format(time_interval)

    query = """SELECT artist_name
                    , artist_msid
                    , artist_mbids
                    , recording_msid
                    , recording_mbid
                    , track_name
                    , COUNT(recording_msid) as listen_count
                 FROM {dataset_id}.{table_id}
                WHERE user_name = @musicbrainz_id
                {time_filter_clause}
             GROUP BY recording_msid, recording_mbid, track_name, artist_name, artist_msid, artist_mbids
             ORDER BY listen_count DESC
                LIMIT {limit}
            """.format(
                dataset_id=config.BIGQUERY_DATASET_ID,
                table_id=config.BIGQUERY_TABLE_ID,
                time_filter_clause=filter_clause,
                limit=config.STATS_ENTITY_LIMIT
            )

    # construct the parameters that must be passed to the Google BigQuery API

    # start with a list of parameters to pass and then convert it to standard format
    # required by Google BigQuery
    parameters = [
        {
            "type": "STRING",
            "name": "musicbrainz_id",
            "value": musicbrainz_id,
        },
    ]

    return stats.run_query(query, parameters)

def get_top_artists(musicbrainz_id, time_interval=None):
    """ Get top artists for user with given MusicBrainz ID over a particular period of time

        Args: musicbrainz_id (str): the MusicBrainz ID of the user
              time_interval  (str): the time interval over which top artists should be returned
                                    (defaults to all time)

        Returns: A sorted list of dicts with the following structure
                [
                    {
                        'artist_name' (str),
                        'artist_msid' (uuid),
                        'artist_mbids' (string of comma-seperated uuids),
                        'listen_count' (int),
                    }
                ]
    """

    filter_clause = ""
    if time_interval:
        filter_clause = "AND listened_at >= TIMESTAMP_SUB(CURRENT_TIME(), INTERVAL {})".format(time_interval)


    query = """SELECT artist_name
                    , artist_msid
                    , artist_mbids
                    , COUNT(artist_msid) as listen_count
                 FROM {dataset_id}.{table_id}
                WHERE user_name = @musicbrainz_id
                {time_filter_clause}
             GROUP BY artist_msid, artist_name, artist_mbids
             ORDER BY listen_count DESC
                LIMIT {limit}
            """.format(
                    dataset_id=config.BIGQUERY_DATASET_ID,
                    table_id=config.BIGQUERY_TABLE_ID,
                    time_filter_clause=filter_clause,
                    limit=config.STATS_ENTITY_LIMIT,
                )

    parameters = [
        {
            'type': 'STRING',
            'name': 'musicbrainz_id',
            'value': musicbrainz_id
        }
    ]

    return stats.run_query(query, parameters)

def get_top_releases(musicbrainz_id, time_interval=None):
    """ Get top releases for user with given MusicBrainz ID over a particular period of time

        Args: musicbrainz_id (str): the MusicBrainz ID of the user
              time_interval  (str): the time interval over which top artists should be returned
                                    (defaults to all time)

        Returns: A sorted list of dicts with the following structure
                [
                    {
                        'artist_name' (str),
                        'artist_msid' (uuid),
                        'artist_mbids' (string of comma seperated uuids),
                        'release_name' (str),
                        'release_msid' (uuid),
                        'release_mbid' (uuid),
                        'listen_count' (int)
                    }
                ]
    """

    filter_clause = ""
    if time_interval:
        filter_clause = "AND listened_at >= TIMESTAMP_SUB(CURRENT_TIME(), INTERVAL {})".format(time_interval)


    query = """SELECT artist_name
                    , artist_msid
                    , artist_mbids
                    , release_name
                    , release_msid
                    , release_mbid
                    , COUNT(release_msid) as listen_count
                 FROM {dataset_id}.{table_id}
                WHERE user_name = @musicbrainz_id
                {time_filter_clause}
             GROUP BY artist_msid, artist_mbids, artist_name, release_name, release_msid, release_mbid
             ORDER BY listen_count DESC
                LIMIT {limit}
            """.format(
                    dataset_id=config.BIGQUERY_DATASET_ID,
                    table_id=config.BIGQUERY_TABLE_ID,
                    time_filter_clause=filter_clause,
                    limit=config.STATS_ENTITY_LIMIT,
                )

    parameters = [
        {
            'type': 'STRING',
            'name': 'musicbrainz_id',
            'value': musicbrainz_id
        }
    ]

    return stats.run_query(query, parameters)

