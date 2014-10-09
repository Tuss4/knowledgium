var knowledgiumControllers = angular.module('knowledgiumControllers', []);

knowledgiumControllers.controller('PostListCtrl', function($scope, $http) {
    $http.get('/api/content/all/').success(function(data)
    {
        $scope.posts = data;
    });
});

knowledgiumControllers.controller('PostDetailCtrl',
['$scope', '$routeParams', '$http',
    function($scope, $routeParams, $http) {
        $http.get('/api/content/' + $routeParams.postId + '/').success(
            function(data) {
                $scope.post = data;
        });
    }]);
