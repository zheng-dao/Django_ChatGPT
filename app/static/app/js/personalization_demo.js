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
request.open('GET', '/api/v1/getads/?cu_id=' + cu_id + '&page=' + page + '&products_owned=' + products_owned + '&ip=' + ip + '&products_recommended=' + products_recommended + '&last_product_url=' + last_product_url + '&zipcode=' + zipcode + '&use_distance_model=' + use_distance_model + '&models=' + models + '&modes=' + modes + '&referrer='+referrer + '&suppress=' + suppress, true)
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
            request.send()

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
