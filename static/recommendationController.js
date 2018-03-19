var myApp = angular.module('myApp', []);
myApp.controller('MyCtrl', function($scope, $http) {
    //$scope.user = "";
    $scope.selected_user = null;

    $scope.user_preferences = [];
    $scope.user_friends = [];
    $scope.recommendations = [];

    $scope.update_data = function () {
        //$scope.user_preferences = [{name: 'Starbucks'}];
        //$scope.user_friends = [{user_id: 2, first_name:'Zarja', last_name:'Cibej'}];
        //$scope.get_user_friends();
        //$scope.get_user_preferences();
        $scope.get_user_friends_and_preferences();
        $scope.get_user_recommendations();
        };


    $scope.get_user_list = function () {
        $http.get('/user_list').then(function(response) {
            $scope.user_list = response.data.user_list;
        });

    };

    $scope.get_user_friends_and_preferences = function () {
        $http.get('/user/'+ $scope.selected_user.user_id.toString() +'/preferences_and_friends').then(function(response) {
            $scope.user_friends = response.data.friends_list;
            $scope.user_preferences = response.data.ratings_list;
        });
    };

    $scope.get_user_recommendations = function () {
        $http.get('/user/'+ $scope.selected_user.user_id.toString() +'/recommendations').then(function(response) {
            $scope.recommendations = response.data.recommendations;
        });

    };

    //$scope.user_list=[{user_id: 0, first_name:'Jure', last_name:'Sokolic'},
    //             {user_id: 1, first_name:'Neja', last_name:'Markocic'},
    //             {user_id: 2, first_name:'Zarja', last_name:'Cibej'}];
    $scope.get_user_list();

    }


);
//TODO: How do we adaptively set request ip?