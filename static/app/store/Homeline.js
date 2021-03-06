Ext.define('Trister.store.Homeline', {
	extend: 'Ext.data.Store',

	config: {
		model: 'Trister.model.Tweet',
        proxy: {
            type: 'ajax',
            url: '/home',
            pageParam: 'page',
            limitParam: 'count',
            reader: {
                type: 'json'
            }
        },
        listeners: {
            load: 'hideLoadingMask'
        }
	},

    hideLoadingMask: function() {
        Ext.getCmp('HomePanel').setMasked(false);
    }
});