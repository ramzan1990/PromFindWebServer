if (!String.prototype.startsWith) {
  String.prototype.startsWith = function(searchString, position) {
    position = position || 0;
    return this.indexOf(searchString, position) === position;
  };
}
String.prototype.count=function(letter) { 
    return this.match( new RegExp(letter,'g') ).length;
}

function saveAs(uri) {
    var link = document.createElement('a');
    if (typeof link.download === 'string' && !isIEorEDGE()) {
        link.href = uri;
        link.setAttribute('download', uri.replace(/^.*[\\\/]/, '') + '.xml');

        //Firefox requires the link to be in the body
        document.body.appendChild(link);

        //simulate click
        link.click();

        //remove the link when done
        document.body.removeChild(link);
    } else {
        window.open(uri);
    }
}

function isIEorEDGE(){
  return navigator.appName == 'Microsoft Internet Explorer' || (navigator.appName == "Netscape" && navigator.appVersion.indexOf('Edge') > -1);
}