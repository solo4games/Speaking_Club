$('<link/>', {
    rel: 'stylesheet', type: 'text/css',
    href: 'https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.7.0/nouislider.css'
}).appendTo('head');
$.getScript('https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.7.0/nouislider.min.js', () => {
    $(function () {
        $('audio').each((i, el) => {
            var $playercont = $(el).closest('.audio-div')
            var slider = $playercont.find('#progress-slider')[0];
            if (typeof slider == "undefined") return;
            el.src = el.src;
            $(el).on("loadedmetadata", function () {
                $playercont.find('.podcastt-time').html(toHHMMSS(el.currentTime) + " / " + toHHMMSS(el.duration));
                $playercont.find('#progress-slider .noUi-handle').attr('data-duration', el.duration).attr('data-current-time', '00:00');
            });
            noUiSlider.create(slider, {
                start: [0],
                range: {
                    'min': [0],
                    'max': [1000]
                },
                step: 1,
                behaviour: 'snap',
                orientation: "horizontal",
                connect: 'lower',
            });
            slider.noUiSlider.on("start", function (values, handle, unencoded, tap, positions, noUiSlider) {
                $(slider).addClass('active');
            });
            slider.noUiSlider.on("end", function (values, handle, unencoded, tap, positions, noUiSlider) {
                $(slider).removeClass('active');
                el.currentTime = (unencoded / 1000) * el.duration;
                $playercont.find('.podcastt-time').html(toHHMMSS(el.currentTime) + " / " + toHHMMSS(el.duration));
            });
            slider.noUiSlider.on("set", function (values, handle, unencoded, tap, positions, noUiSlider) {
                if (el.paused) {
                    el.currentTime = (unencoded / 1000) * el.duration;
                    $playercont.find('.podcastt-time').html(toHHMMSS(el.currentTime) + " / " + toHHMMSS(el.duration));
                };
            });
            slider.noUiSlider.on("update", function (values, handle, unencoded, tap, positions, noUiSlider) {
                let duration = $playercont.find('.noUi-handle').attr('data-duration');
                let q = unencoded * duration / 1000;
                $playercont.find('.noUi-handle').attr('data-current-time', toHHMMSS(q));
            });

            $playercont.find('.podcastt-playpause').on('click', function () {
                let that = this;
                let audio = $playercont.find('audio').get(0);
                if ($(this).hasClass('playing')) {
                    $(this).removeClass('playing');
                    audio.pause();
                    $(audio).off('timeupdate');
                } else {
                    $(this).addClass('playing');
                    audio.play();
                    $(audio).on('timeupdate', function () {
                        let q = this.currentTime / this.duration;
                        if (q == 1) {
                            $playercont.find('.podcastt-playpause').removeClass('playing');
                        }
                        let $progressSlider = $playercont.find('#progress-slider:not(:has(.noUi-active))');
                        if ($progressSlider.length) {
                            $progressSlider[0].noUiSlider.set(1000 * q)
                            $progressSlider.find('.noUi-handle').attr('data-current-time', toHHMMSS(this.currentTime));
                            $playercont.find('.podcastt-time').html(toHHMMSS(this.currentTime) + " / " + toHHMMSS(this.duration))
                        }
                    });
                }
            });
            $playercont.find('.podcastt-speed a').on('click', function () {
                $(this).siblings().removeClass('active');
                $(this).addClass('active');
                let audio = $playercont.find('audio').get(0);
                if ($(this).hasClass('podcastt-speed-5')) {
                    audio.playbackRate = 0.5;
                }
                else if ($(this).hasClass('podcastt-speed-10')) {
                    audio.playbackRate = 1;
                }
                else if ($(this).hasClass('podcastt-speed-15')) {
                    audio.playbackRate = 1.5;
                }
                else if ($(this).hasClass('podcastt-speed-20')) {
                    audio.playbackRate = 2;
                }
            });

        });

        function toHHMMSS(sec) {
            var sec_num = parseInt(sec, 10);
            var hours = Math.floor(sec_num / 3600);
            var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
            var seconds = sec_num - (hours * 3600) - (minutes * 60);

            if (hours < 10) { hours = "0" + hours; }
            if (minutes < 10) { minutes = "0" + minutes; }
            if (seconds < 10) { seconds = "0" + seconds; }
            return hours == "00" ? minutes + ':' + seconds : hours + ':' + minutes + ':' + seconds;
        }

    });
});