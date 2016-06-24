module.exports = function(gulp, paths, prefixer, rename, minifyCss, sass, browserSync, bsName, sourcemaps) {
    'use strict';
    var bs;

    if (browserSync.has(bsName)) {
        bs = browserSync.get(bsName);
    } else {
        bs = browserSync.create(bsName);
    }

    /*
      Compiles sass to css with source maps
      then prefixes
      -> main.css
      then minifies
      -> main.min.css
    */
    gulp.task('sass', function() {
        return gulp.src(paths.sass.main)
            .pipe(sourcemaps.init())
            .pipe(sass({errLogToConsole: true}).on('error', sass.logError))
            .pipe(prefixer())
            // .pipe(sourcemaps.write('.'))
            .pipe(gulp.dest(paths.sass.dest))
            .pipe(bs.stream())
            .pipe(minifyCss({
                keepSpecialComments: 0
            }))
            .pipe(rename({ extname: '.min.css' }))
            // .pipe(sourcemaps.write('.'))
            .pipe(gulp.dest(paths.sass.dest));
            // .pipe(bs.stream());
    });
};
