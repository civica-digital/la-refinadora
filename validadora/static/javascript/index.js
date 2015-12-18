var app = new Vue({
    el: "#app",
    data: {
      dataset: {
          url: "",
          valid: true,
          reasons: []
      },
      callback: {
          url: "",
          valid: true,
          reasons: []
      },
      validators: {
          list: [],
          reasons: []
      }
    },
    methods: {
      validateDataset: function () {
          if(this.dataset.url == "") {
                var msg = "Este campo no debe estar vacio";
                this.dataset.valid = false;


                if (-1 == this.dataset.reasons.indexOf(msg)) {
                    this.dataset.reasons.push(msg);
                }
                notificationCenter.error(msg, 8000);

                return false;
            } else {
                notificationCenter.remove("Este campo no debe estar vacio");
            }

        return this.validateFieldURL("dataset");
      },
      validateCallback: function(){
          return this.validateFieldURL("callback");
      },
      validateFieldURL:    function (field) {
            var status = true;

            if(!isUrlValid(this[field].url)) {
              var msg = "Debe contener una url valida";
              this[field].valid = false;
              if (-1 == this[field].reasons.indexOf(msg)) {
                  this[field].reasons.push(msg);
              }
              notificationCenter.error(msg, 8000);
              status = false;
            } else {
                notificationCenter.remove(msg);
            }

            if (status) {
                this[field].valid = true;
                this[field].reasons = [];
            }

            return status;
      },
      validateValidators: function(){
          var status = true;

          if(this.validators.list.length == 0) {
              var msg = "Debes seleccionar al menos un validador";
              if (-1 == this.validators.reasons.indexOf(msg)) {
                  this.validators.reasons.push(msg)
              }
              notificationCenter.error(msg, 8000);
              status = false
          } else {
              console.log("removiendo")
              notificationCenter.remove("Debes seleccionar al menos un validador");
          }
          return status;
      },
      onSubmit: function()   {
          var dataset = this.validateDataset();
          var validators =  this.validateValidators();
          if (dataset && validators) {
              $("[name=validate]").submit();
          }
      }
    }
});

function isUrlValid(url) {
    return /^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url);
}

notificationCenter = new (function() {
    var state = {};
    this.notify = function (msg, time, style)
    {
        if(!state[msg])
            Materialize.toast(msg, time, style);
        state[msg] = true;
        setTimeout(function() {
            state[msg] = false
        },
        time + 1000);
    };

    this.warning = function(msg, time) {
        this.notify(msg, time, 'yellow lighten-2')
    };


    this.error = function(msg, time) {
        this.notify(msg, time, 'red darken-2')
    };


    this.success = function(msg, time) {
        this.notify(msg, time, 'green accent-4')
    };

    this.debug = function(msg, time) {
        this.notify(msg, time, 'blue darken-4')
    };

    this.remove = function(msg) {
        try {
            $('div:contains("' + msg + '")')[1].remove();
            state[msg] = false
        }catch (e) {};
    };
})();


