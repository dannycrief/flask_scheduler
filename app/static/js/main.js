$(document).ready(function () {
    const hiddenElement = $('.hidden').css('display', 'none');
    $('.continueButton').on('click', function () {
        const subject = $('#subject');
        const description = $('#description');
        const start_time = $('#start_time');
        const end_time = $('#end_time');

        let subject_str = [];
        let description_str = [];
        let start_time_str = [];
        let end_time_str = [];

        subject_str.push(subject.val());
        description_str.push(description.val());
        start_time_str.push(start_time.val());
        end_time_str.push(end_time.val());


        const request = $.ajax({
            url: "/subject_description",
            type: "POST",
            data: {
                subject: subject_str[0],
                description: description_str[0],
                start_time: start_time_str[0],
                end_time: end_time_str[0]
            },
        });

        request.done(function (data) {
            $('.show').fadeOut("slow", function () {
                $(this).css('display', 'none')
                $(hiddenElement).fadeIn("slow", function () {
                    $(this).css('display', 'flex')
                });
            });
        });
    });
});