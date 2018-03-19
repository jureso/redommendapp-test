var myApp = angular.module('RecommendApp', []);
myApp.controller('RecommendCtrl', function($scope, $http) {

        $scope.selected_user = null;
        $scope.user_preferences = [];
        $scope.user_friends = [];
        $scope.recommendations = [];

        $scope.update_data = function () {
            $scope.get_user_preferences_and_friends();
            $scope.get_user_recommendations();
        };

        $scope.get_user_list = function () {
            $http.get('/user_list').then(
                function successCallback(response) {
                    $scope.user_list = response.data.user_list;
                },
                function errorCallback(response) {
                    console.log(response.status, response.statusText);
                });
        };
        $scope.get_user_preferences_and_friends = function () {
            $http.get('/user/' + $scope.selected_user.user_id.toString() + '/preferences_and_friends').then(
                function successCallback(response) {
                    $scope.user_friends = response.data.friends_list;
                    $scope.user_preferences = response.data.ratings_list;
                },
                function errorCallback(response) {
                    console.log(response.status, response.statusText);
                });
        };
        $scope.get_user_recommendations = function () {
            $http.get('/user/' + $scope.selected_user.user_id.toString() + '/recommendations').then(
                function successCallback(response) {
                    $scope.recommendations = response.data.recommendations;
                },
                function errorCallback(response) {
                    console.log(response.status, response.statusText);
                });
        };

        $scope.get_user_list();
    }
);