<template>
</template>
<script>

    import {setIdToken, setAccessToken} from '../../utils/auth';
    import {getUserInfo} from "../../utils/django-api";

    export default {
        name: '',
        mounted() {
            this.$nextTick(() => {
                setAccessToken();
                setIdToken();
                getUserInfo().then((response) => {
                    let json = JSON.parse(JSON.stringify(response))
                    if (json['credential_is_valid'] === true) {
                        window.location.href = '/';
                    } else {
                        window.location.href = '/settings';
                    }
                });
            });
        },
    };
</script>
