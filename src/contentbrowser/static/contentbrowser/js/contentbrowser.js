
function ContentBrowser(options) {
    var self = this, $cb_el,
        defaultOptions = {
            name: null,
            field_id: null,
            cb_element: null,
            static_prefix: null
        };

    /** Extend the default options **/
    if (typeof options === 'object') {
        options = django.jQuery.extend(defaultOptions, options);
    } else {
        options = defaultOptions;
    }

    /** Private **/
    $cb_el = django.jQuery(options.cb_element);

    /** Public **/
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
        self.showLoader(options.cb_element + ' .cb_items_panel');
        django.jQuery.ajax({
            url: url,
            success: function(data) {
                django.jQuery(options.cb_element + ' .cb_items_panel').empty().html(data);
            }
        });
        return false;
    };


    /** Event Handlers **/
    $cb_el.find('.cb_types_panel a').click(function() {
        $cb_el.find('.cb_types_panel li a').removeClass('selected');
        $(this).addClass('selected');
        return self.loadItems($(this).attr('href'));        
    });


    $cb_el.find('.cb_toggle_panels').click(function() {
        var panels = $cb_el.find('.cb_panels');
        if (panels.is(':visible')) {
            panels.slideUp(300);
        } else {
            panels.slideDown(300);
        }
        return false;
    });


    $cb_el.find('.cb_items_panel .pagination a').live('click', function() {
        return self.loadItems($(this).attr('href'));
    });

}

