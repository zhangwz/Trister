Ext.define('Trister.view.Homeline', {
    extend: 'Ext.List',
    xtype: 'homelinelist',
    requires: [
        'Trister.store.Homeline',
        'Ext.plugin.ListPaging',
        'Ext.plugin.PullRefresh'
    ],

    config: {
        title: 'Home',
        iconCls: 'home',
        cls: 'home',
        store: 'Homeline',
        disableSelection: true,
        plugins: [
            { xclass: 'Ext.plugin.ListPaging' },
            { xclass: 'Ext.plugin.PullRefresh' }
        ],
        emptyText: '<p class="no-tweets">No tweets found!</p>',
        itemTpl: Ext.create('Trister.view.template.HomelineTweet',{})
    }
});