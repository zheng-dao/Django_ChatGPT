var _utilsSvc = epi.EPiServer.Forms.Utils,
    originalGetCustomElementValue = epi.EPiServer.Forms.Extension.getCustomElementValue,
    originalBindCustomElementValue = epi.EPiServer.Forms.Extension.bindCustomElementValue

$.extend(true, epi.EPiServer.Forms, {

    /// extend the Validator to validate Visitor's value in Clientside.
    /// Serverside's Fullname of the Validator instance is used as object key (Case-sensitve) to lookup the Clientside validate function.        
    Validators: {
        "Web.Business.RecaptchaValidator": function (fieldName, fieldValue, validatorMetaData) {
            // validate recaptcha element
            if (fieldValue) {
                return { isValid: true };
            }

            return {isValid: false, message: 'Invalid captcha value.' };
        }
    },
    Extension: {
        getCustomElementValue: function ($element) {

             if ($element.hasClass("FormRecaptcha")) {
                // for recaptcha element
                 var widgetId = $element.data("epiforms-recaptcha-widgetid");
                if (widgetId !== undefined && grecaptcha) {
                    return grecaptcha.getResponse(widgetId);
                } else {
                    return null;
                }
            }
            // if current element is not our job, let others process
            return originalGetCustomElementValue.apply(this, [$element]);
        }
    }
});
