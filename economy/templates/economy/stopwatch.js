{% load cron_tags %}

    (function() {

  function pad(num) {
    return ("0" + parseInt(num)).substr(-2);
  }

  function tick() {
    later.date.localTime();
    cron_list = '{% cron_tag %}'.split(' ');
    var weekday = cron_list.splice(2, 1)
    cron_list.push(weekday)
    var cron_str = cron_list.join(' ')
    var s = later.parse.cron(cron_str);
    var s = later.schedule(s).next();

    var now = new Date;

    var remain = ((s - now) / 1000);
    var days =  Math.floor(remain / 60 / 60 / 24)
    var dd = parseInt(days);
    var hh = pad((remain / 60 / 60) % 24);
    var mm = pad((remain / 60) % 60);
    var ss = pad(remain % 60);

    if (days !== 0) {
    document.getElementById('time').innerHTML =
     dd + "d " + hh + ":" + mm + ":" + ss;}
    else {
    document.getElementById('time').innerHTML =
     hh + ":" + mm + ":" + ss;}
    setTimeout(tick, 1000);
  }
  document.addEventListener('DOMContentLoaded', tick);
})();
