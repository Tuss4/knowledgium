var knowledgiumApp = angular.module('knowledgiumApp', [
    'ngRoute',
    'knowledgiumControllers'
]);

knowledgiumApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/posts', {
                templateUrl: 'partials/post_list.html',
                controller: 'PostListCtrl'
            }).
            when('/posts/:postId', {
                templateUrl: 'partials/post_detail.html',
                controller: 'PostDetailCtrl'
            }).
            otherwise({
                redirectTo: '/posts'
            })
}]);
