/**
 * Payee Search
 * Author: Pasquale Scerbo (pscerbo@extractable.com)
 * BOKFOB-110 Change Request
 */

$(function () {
    $("#payeeSearch").on("keyup click input", function () {
        // Retrieve the input field text and reset the count to zero
        var $filter = $(this).val(),$numOfPayeesFound = 0,$searchHiddenPayees = ($('#showHidden').is(':checked'));
        // Loop through the comment list
        $(".payee .payeeName h2 a").each(function () {
            // If the list item does not contain the text phrase fade it out
            if ($(this).text().search(new RegExp($filter, "i")) < 0) {
                $(this).parents(".payee").hide();
            } else {
                if ($searchHiddenPayees) {
                    $(this).parents(".payee").show();
                    $numOfPayeesFound++;
                }
                else
                {
                    if (!$(this).parents(".payee").hasClass('hiddenPayee'))
                    {
                        $(this).parents(".payee").show();
                        $numOfPayeesFound++;
                    }
                }
            }
        });

        // Update the count
        //var numberItems = $numOfPayeesFound;
        if ($numOfPayeesFound == 0) {
            $(".payeeFlash").hide();
            $(".noPayeeFound").delay(500).show();
        } else {
            if ($filter != "")
            { $(".payeeFlash").show(); }
            else
            { $(".payeeFlash").hide(); }
            $(".noPayeeFound").hide();
        }
    });

    //Clear Payee Search Field
    $(".clearInput").on("click", function () {
        //$(this).prev().val("");
        $("#payeeSearch").val("");
        $(".payee").show();
        $(".viewAllPayments").parent().hide();
    });

    $(".viewAllPayments").on("click", function (e) {
        //$(this).prev().val("");
        $("#payeeSearch").val("");
        $(".payee").show();
        $(this).parent().hide();
        e.preventDefault();
    });

    $("#showHidden").change(function () {
        if ($(this).is(':checked')) {
            $(".payee").each(function () {
                $(this).show();
            });
        } else {
            $(".hiddenPayee").each(function () {
                $(this).hide();
            });
        }
        // initiate the serach
        if($('#payeeSearch').val() != "")
        {
            $('#payeeSearch').trigger('click');
        }
    });
});
