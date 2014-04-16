define(['jquery'], function($) {
    return {
        //http://stackoverflow.com/questions/16941104/remove-a-parameter-to-the-url-with-javascript
        removeURLParameter : function(url, param) {
         var urlparts= url.split('?');
         if (urlparts.length>=2)
         {
          var prefix= encodeURIComponent(param)+'=';
          var pars= urlparts[1].split(/[&;]/g);
          for (var i=pars.length; i-- > 0;)
           if (pars[i].indexOf(prefix, 0)==0)
            pars.splice(i, 1);
          if (pars.length > 0)
           return urlparts[0]+'?'+pars.join('&');
          else
           return urlparts[0];
         }
         else
          return url;
        },



        //http://stackoverflow.com/questions/6953944/how-to-add-parameters-to-a-url-that-already-contains-other-parameters-and-maybe
        addParameter: function(url, parameterName, parameterValue, atStart/*Add param before others*/){
            replaceDuplicates = true;
            if(url.indexOf('#') > 0){
                var cl = url.indexOf('#');
                urlhash = url.substring(url.indexOf('#'),url.length);
            } else {
                urlhash = '';
                cl = url.length;
            }
            sourceUrl = url.substring(0,cl);

            var urlParts = sourceUrl.split('?');
            var newQueryString = '';

            if (urlParts.length > 1)
            {
                var parameters = urlParts[1].split('&');
                for (var i=0; (i < parameters.length); i++)
                {
                    var parameterParts = parameters[i].split('=');
                    if (!(replaceDuplicates && parameterParts[0] == parameterName))
                    {
                        if (newQueryString == '')
                            newQueryString = '?';
                        else
                            newQueryString += '&';
                        newQueryString += parameterParts[0] + '=' + (parameterParts[1]?parameterParts[1]:'');
                    }
                }
            }
            if (newQueryString == '')
                newQueryString = '?';

            if(atStart){
                newQueryString = '?'+ parameterName + '=' + parameterValue + (newQueryString.length>1?'&'+newQueryString.substring(1):'');
            } else {
                if (newQueryString !== '' && newQueryString != '?')
                    newQueryString += '&';
                newQueryString += parameterName + '=' + (parameterValue?parameterValue:'');
            }
            return urlParts[0] + newQueryString + urlhash;
        }

    }
})