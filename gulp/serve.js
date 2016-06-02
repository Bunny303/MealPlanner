module.exports = function(gulp, paths, browserSync, bsName) {
    'use strict';
    var bs, reload;

    if (browserSync.has(bsName)) {
        bs = browserSync.get(bsName);
    } else {
        bs = browserSync.create(bsName);
    }

    reload = bs.reload;

    gulp.task('serve', ['sass'], function() {
        bs.init({
            proxy: 'localhost:8000'
        });

        gulp.watch(paths.sass.watch, ['sass']);
        gulp.watch(paths.templates.watch).on('change', reload);
        gulp.watch(paths.js.watch).on('change', reload);
    });
};
