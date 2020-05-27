filepath = 'csvfiles/test.csv';
const spawn = require('child_process').spawn;
const pyProcess = spawn('python', ['assets/valve.py', filepath]);

var list = [];


pyProcess.stdout.on('data', function(data)
{
    list = data.toString().split("\r\n");
    var n = parseInt(list[0])
    var numbers = list.slice(1,-1);
    console.log(n);
    for(i = 0; i < numbers.length; i++)
       console.log(numbers[i]);
    console.log(list);
});


