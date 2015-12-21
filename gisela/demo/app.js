angular.module('giselaApp', [])
    .factory('Tags', function() {
        var items = [];
        return {
            getItems: function() {
                return items;
            },
            addTag: function(tag) {
                items.push(tag);
            }
        }
    })
    .factory('Timelog', function() {
        var items = [];
        return {
            getItems: function() {
                return items;
            },
            addTime: function(time) {
                items.push(time);
            },
            sum: function() {
                return items.reduce(function(total, article) {
                    return total + time.duration;
                }, 0)
            }
        }
    })
    .controller('TagsList', function($scope, $http, Tags){
        $http.get('/tags').then(function(tagsResponse) {
            $scope.tags = tagsResponse.data;
        })
    })
    .controller('TimesList', function($scope, $http, Timelog){
        $http.get('/times').then(function(timesResponse) {
        $scope.times = timesResponse.data;})
    })
;
