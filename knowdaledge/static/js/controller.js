var knowledgiumControllers = angular.module('knowledgiumControllers', []);

knowledgiumControllers.controller('PostListCtrl', function($scope, $http) {
    $http.get('http://localhost:8080/api/content/all/').success(function(data)
    {
        $scope.posts = data;
    });
});

knowledgiumControllers.controller('PostDetailCtrl',
['$scope', '$routeParams',
    function($scope, $routeParams) {
        $scope.postId = $routeParams.postId;
}]);
