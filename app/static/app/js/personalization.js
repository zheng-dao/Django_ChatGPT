    var request = new XMLHttpRequest();
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var cu_id = urlParams.get('cu_id');
    var page = urlParams.get('page');
    var products_owned = urlParams.get('products_owned');
    var products_recommended = urlParams.get('products_recommended');
    var ip = urlParams.get('ip');
    var last_product_url = urlParams.get('last_product_url');
    var zipcode = urlParams.get('zipcode');
    var use_distance_model = urlParams.get('use_distance_model');
    var models = urlParams.get('models');
    var modes = urlParams.get('modes');
    var referrer = urlParams.get('referrer');
    var suppress = urlParams.get('suppress');
    var data_post = urlParams.get('data');
    var ml_version = urlParams.get('ml_version');
    var session_init = urlParams.get('session_init');
            if (cu_id == null) {
        cu_id = '24212';
            }
            if (page == null) {
                page = '';
            }
            if (ip == null) {
        ip = '';
            }
            if (products_recommended == null) {
        products_recommended = '';
            }
            if (products_owned == null) {
        products_owned = '';
            }
            if (last_product_url == null) {
        last_product_url = '';
            }
            if (zipcode == null) {
        zipcode = '';
            }
            if (use_distance_model == null) {
        use_distance_model = '';
            }
            if (models == null) {
        models = '';
            }
            if (modes == null) {
                modes = '';
            }
            if (referrer == null) {
        referrer = '';
            }
        if (suppress == null) {
            suppress = '';
        }
        if (data_post == null) {
            data_post = '';
        }
        if (ml_version == null) {
            ml_version = '';
        }
        if (session_init == null) {
                    session_init = '';
        }
request.open('GET', '/api/v1/getads/?cu_id=' + cu_id + '&page=' + page + '&products_owned=' + products_owned + '&ip=' + ip + '&products_recommended=' + products_recommended + '&last_product_url=' + last_product_url + '&zipcode=' + zipcode + '&use_distance_model=' + use_distance_model + '&models=' + models + '&modes=' + modes + '&referrer='+referrer + '&suppress=' + suppress + '&data=' + data_post + '&ml_version=' + ml_version + '&session_init=' + session_init, true)
            request.onload = function () {
                // Begin accessing JSON data here
                var data = JSON.parse(this.response);
                console.log('look here')
                console.log(data)
                if (request.status >= 200 && request.status < 400) {
                    //console.log(data);
                    document.getElementById('ads').innerHTML = JSON.stringify(data);
                } else {
                    console.log('error');
                }
            }
            request.send();
            function show(param_div_id) {
                var i;
                var ads = JSON.parse(document.getElementById(param_div_id).innerHTML);
                //alert(ads);
                for (i = 0; i < ads.length; i++) {
                    //alert(ads[i]);
                    document.getElementById(ads[i].div_id).innerHTML = ads[i].ad_html;
                    var geo = ads[i].geo;
                    if (geo != null) {
                        var a = document.getElementById(ads[i].div_id).getElementsByTagName("a");
                        a[0].innerHTML = geo;
                    }
                }
            }
            //alert('hello');
            setTimeout(show, 10000)
            show('ads');
