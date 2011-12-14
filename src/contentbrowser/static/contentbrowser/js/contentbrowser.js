
function ContentBrowser(options) {
    var self = this,
        defaultOptions = {
            name: null,
            field_id: null,
            static_prefix: null
        };

    /** Extend the default options **/
    if (typeof options === 'object') {
        options = django.jQuery.extend(defaultOptions, options);
    } else {
        options = defaultOptions;
    }

    /** Private parts **/

    /** Public parts **/
    this.showLoader = function(container) {
        var loader_path = options.static_prefix + 'contentbrowser/img/ajax-loader.gif';
        django.jQuery(container).empty()
            .html('<div style="text-align:center;"><img src="' + loader_path + '" /></div>');
    }

    this.takeAction = function(action, el) {
        return cb_actions[action](django.jQuery(el), options.field_id);
    };
    
    this.loadItems = function(url) {
        url += '&cb=cb_' + options.name;
        self.showLoader('#cb_items_panel');
        django.jQuery.ajax({
            url: url,
            success: function(data) {
                django.jQuery('#cb_items_panel').empty().html(data);
            }
        });
        return false;
    };

}


django.jQuery(document).ready(function() {

    django.jQuery('#cb_toggle_panels').click(function() {
        django.jQuery('#cb_types_panel, #cb_items_panel, #cb_display_panel, #cb_filter_panel')
            .toggle(300);
        return false;
    });

});
