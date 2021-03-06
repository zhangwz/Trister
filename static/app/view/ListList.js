Ext.define('Trister.view.ListList', {
    extend: 'Ext.List',
    xtype: 'listlist',

    requires: [
        'Trister.store.ListList',
        'Ext.plugin.PullRefresh'
    ],

    config: {
        id: 'ListList',
        title: 'List',
        cls: 'tweet-list-list',
        store: 'ListList',
        grouped: true,
        disableSelection: true,
        scrollToTopOnRefresh: false,
        plugins: [
            {
                xclass: 'Ext.plugin.PullRefresh',
                pullRefreshText: 'Pull down to update...',
                releaseRefreshText: 'Release to update...'
            }
        ],
        emptyText: '<p class="no-tweets">No Lists found!</p>',
        itemTpl: Ext.XTemplate.from('ListAbstract')
    }
});