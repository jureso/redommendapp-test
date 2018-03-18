var myApp = angular.module('myApp', []);
myApp.controller('MyCtrl', function($scope, $http) {
    //$scope.user = "";
    $scope.selected_user = "";

    $scope.user_preferences = [{name: 'McDonalds'}, {name: 'Wahaca'}];
    $scope.user_friends = [{user_id: 1, first_name:'Neja', last_name:'Markocic'}];

    $scope.update_data = function () {
        //$scope.user_preferences = [{name: 'Starbucks'}];
        //$scope.user_friends = [{user_id: 2, first_name:'Zarja', last_name:'Cibej'}];
        $scope.get_user_friends();
        $scope.get_user_preferences();
        };


    $scope.get_user_list = function () {
        $http.get('/user_list').then(function(response) {
            $scope.user_list = response.data.user_list;
        });

    };

    $scope.get_user_friends = function () {
        $http.get('/user/'+ $scope.selected_user.user_id.toString() +'/friends').then(function(response) {
            $scope.user_friends = response.data.friends;
        });
    };

    $scope.get_user_preferences = function () {
        $http.get('/user/'+ $scope.selected_user.user_id.toString() +'/preferences').then(function(response) {
            $scope.user_preferences = response.data.preferences;
        });
    };

    $scope.get_user_recommendations = function () {};

    //$scope.user_list=[{user_id: 0, first_name:'Jure', last_name:'Sokolic'},
    //             {user_id: 1, first_name:'Neja', last_name:'Markocic'},
    //             {user_id: 2, first_name:'Zarja', last_name:'Cibej'}];
    $scope.get_user_list();

    }


);
//TODO: How do we adaptively set request ip?