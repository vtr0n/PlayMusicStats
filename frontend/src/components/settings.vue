<template>
  <div>
    <app-nav></app-nav>
    <br>
    <div class="col-sm-12" v-show="isLoggedIn()">
      <div class="jumbotron text-center" v-if="isLoggedIn()">
        <div class="offset-sm-3 col-sm-6">
          <b-alert
            variant="danger"
            dismissible
            fade
            :show="errorAlert"
            @dismissed="errorAlert=false"
          >
            {{errorAlertMessage}}
          </b-alert>
          <b-input-group prepend="" class="mt-3">
            <b-form-input :placeholder="code" v-model="apiKey">{apiKey}</b-form-input>
            <b-input-group-append>
              <b-button variant="outline-success" @click="getAuthUrl()">Get API key</b-button>
              <b-button variant="info" @click="checkCode()" v-model="confirmButton">{{ confirmButton }}</b-button>
            </b-input-group-append>
          </b-input-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import AppNav from './AppNav';
    import {isLoggedIn} from '../../utils/auth';
    import {getAuthUrl, confirmCode, getUserInfo} from '../../utils/django-api';

    export default {
        name: 'settings',
        components: {
            AppNav,
        },
        created() {
            this.getInfo()
        },
        data() {
            return {
                errorAlert: false,
                errorAlertMessage: 'Something wrong',
                apiKey: '',
                confirmButton: 'Confirm Code',
                code: 'Enter your API key',
            };
        },
        methods: {
            isLoggedIn() {
                return isLoggedIn();
            },
            getInfo() {
                getUserInfo().then((response) => {
                    let json = JSON.parse(JSON.stringify(response))
                    if (json['credential_is_valid'] === true) {
                        this.confirmButton = 'Update Code'
                        this.code = json['code']
                    } else {
                        this.confirmButton = 'Confirm Code'
                    }

                });

            },
            getAuthUrl() {
                getAuthUrl().then((response) => {
                    let json = JSON.parse(JSON.stringify(response))
                    window.open(
                        json['url'],
                        '_blank' // <- This is what makes it open in a new window.
                    );
                });
            },

            checkCode() {
                confirmCode(this.apiKey).then((response) => {
                    if (response.status !== 200) {
                        this.errorAlert = true;
                        this.errorAlertMessage = response.response.data;
                    } else {
                        window.location.href = '/';
                    }
                });
            }
        },
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
