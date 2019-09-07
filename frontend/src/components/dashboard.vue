<template>

  <div>
    <app-nav></app-nav>
    <br>
    <div class="col-sm-12">
      <div class="jumbotron text-center">
        <div class="row">
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Listening time per day</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{dayMusicDuration}}</h6>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Listening time per week</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{weekMusicDuration}}</h6>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Listening time per month</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{monthMusicDuration}}</h6>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Listening time for all time</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{allMusicDuration}}</h6>
              </div>
            </div>
          </div>
        </div>

        <br>

        <div class="row">
          <div class="col-sm-12">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Listening time per week</h5>
                <!--        <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>-->
                <div id="app">
                  <ve-line :data="chartData" :settings="chartSettings" :extend="chartExtend"></ve-line>
                </div>
              </div>
            </div>
          </div>
        </div>

        <br>

        <div class="row">
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Top artist by month</h5>
                <b-table striped hover :items="items4" thead-class="hidden_header">
                  <template slot="[artist_art_ref]" slot-scope="data">
                    <b-img thumbnail :src=data.item.artist_art_ref></b-img>
                  </template>
                </b-table>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Top artist for all time</h5>
                <b-table striped hover :items="items2" thead-class="hidden_header">
                  <template slot="[artist_art_ref]" slot-scope="data">
                    <b-img thumbnail :src=data.item.artist_art_ref></b-img>
                  </template>
                </b-table>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Top tracks by month</h5>
                <b-table striped hover :items="items3" thead-class="hidden_header">
                  <template slot="[album_art_ref]" slot-scope="data">
                    <b-img thumbnail :src=data.item.album_art_ref></b-img>
                  </template>
                </b-table>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Top tracks for all</h5>
                <div>
                  <b-table striped hover :items="items" thead-class="hidden_header">
                    <template slot="[album_art_ref]" slot-scope="data">
                      <b-img thumbnail :src=data.item.album_art_ref></b-img>
                    </template>
                  </b-table>
                </div>

              </div>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>
<script>

    import VeLine from 'v-charts/lib/line.common'
    import AppNav from './AppNav';
    import {getStats} from '../../utils/django-api';

    export default {
        components: {
            VeLine,
            AppNav
        },
        created() {
            this.getMyStats()
        },
        data() {
            this.chartSettings = {
                area: true
            };
            this.chartExtend = {
                legend: {
                    selected: {
                        hours: true,
                        minutes: false
                    }
                }
            };
            return {
                chartData: {
                    columns: ['date', 'hours', 'minutes'],
                    rows: [
                        {'date': '00.00', 'hours': 0, 'minutes': 0},
                    ]
                },
                items: [],
                items2: [],
                items3: [],
                items4: [],
                allMusicDuration: 'Unknown',
                dayMusicDuration: 'Unknown',
                weekMusicDuration: 'Unknown',
                monthMusicDuration: 'Unknown',
            }
        },
        methods: {
            prettyTime(time) {
                let allMusicDuration = 'Unknown';
                if (time > 0) {
                    if (time < 60) { // < 1 minute
                        return allMusicDuration = time + 's'
                    }
                    if (time < 60 * 60) {
                        return allMusicDuration = Math.floor(time / 60) + 'm'
                    }
                    if (time < 60 * 60 * 24) {
                        let hours = Math.floor(time / (60 * 60));
                        let minutes = time - (60 * 60 * hours);
                        minutes = Math.floor(minutes / 60);
                        if (minutes === 0) {
                            return allMusicDuration = hours + 'h'
                        }
                        return allMusicDuration = hours + 'h ' + minutes + 'm'
                    }
                    let days = Math.floor(time / (60 * 60 * 24));
                    let hours = time - Math.floor(60 * 60 * 24 * days);
                    hours = Math.floor(hours / (60 * 60));
                    let minutes = time - ((60 * 60 * 24 * days) + (60 * 60 * hours));
                    minutes = Math.floor(minutes / 60);
                    if (minutes === 0) {
                        if (hours === 0)
                            return allMusicDuration = days + 'd';
                        return allMusicDuration = days + 'd ' + hours + 'h'
                    }
                    if (hours === 0) {
                        return allMusicDuration = days + 'd ' + minutes + 'm'
                    }
                    return allMusicDuration = days + 'd ' + hours + 'h ' + minutes + 'm'
                }
                return allMusicDuration
            },
            getMyStats() {
                getStats().then((response) => {
                    let json = JSON.parse(JSON.stringify(response));

                    this.allMusicDuration = this.prettyTime(json['all_duration_sec']);
                    this.dayMusicDuration = this.prettyTime(json['duration_by_day_sec']);
                    this.weekMusicDuration = this.prettyTime(json['duration_by_day_week']);
                    this.monthMusicDuration = this.prettyTime(json['duration_by_day_month']);

                    let tracks = [];
                    for (var i = 0; i < json['top_tracks'].length; i++) {
                        tracks[i] = json['top_tracks'][i];
                        tracks[i]['new'] = tracks[i]['artist'] + " - " + tracks[i]['title'] + " (" + tracks[i]['play_count'] + ")";
                        delete tracks[i]['artist'];
                        delete tracks[i]['title'];
                        delete tracks[i]['play_count'];
                    }
                    this.items = tracks;

                    let tracks2 = [];
                    for (var i = 0; i < json['top_tracks_by_mouth'].length; i++) {
                        tracks2[i] = json['top_tracks_by_mouth'][i];
                        tracks2[i]['new'] = tracks2[i]['artist'] + " - " + tracks2[i]['title'] + " (" + tracks2[i]['play_count'] + ")";
                        delete tracks2[i]['artist'];
                        delete tracks2[i]['title'];
                        delete tracks2[i]['play_count'];
                    }
                    this.items3 = tracks2;

                    let artists = [];
                    for (var i = 0; i < json['top_artists'].length; i++) {
                        artists[i] = json['top_artists'][i];
                        artists[i]['new'] = artists[i]['artist'] + " (" + artists[i]['play_count'] + ")";
                        delete artists[i]['artist'];
                        delete artists[i]['play_count'];
                    }
                    this.items2 = artists


                    let artists2 = [];
                    for (var i = 0; i < json['top_artists_by_mouth'].length; i++) {
                        artists2[i] = json['top_artists_by_mouth'][i];
                        artists2[i]['new'] = artists2[i]['artist'] + " (" + artists2[i]['play_count'] + ")";
                        delete artists2[i]['artist'];
                        delete artists2[i]['play_count'];
                    }
                    this.items4 = artists2


                    this.chartData = json['chart']
                });
            }
        }
    }


</script>

<style>
  .small {
    max-width: 600px;
    margin: 150px auto;
  }
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
<style>
  .hidden_header {
    display: none;
  }
</style>
