"use strict";

var gulp = require('gulp');
// var sass = require('gulp-ruby-sass');
var sass = require('gulp-sass');
var browserSync = require('browser-sync');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');

const env = (process.env.NODE_ENV === 'production' ? 'production' : 'development');

const SRC_BASE = 'src/';
const SRC_HTML = SRC_BASE + 'templates/*.html';
const SRC_SASS = SRC_BASE + 'styles/*.scss';
const SRC_JS = SRC_BASE + 'scripts/*.js';
const SRC_TO_WATCH = [SRC_HTML, SRC_SASS, SRC_JS];
const DEST_BASE = 'builds/'+env+'/';
const DEST_TEMPLATES = DEST_BASE;
const DEST_STYLES = DEST_BASE + 'css/';
const DEST_SCRIPTS = DEST_BASE + 'js/';

gulp.task('html', () => {
	gulp.src(SRC_HTML)
		.pipe(gulp.dest(DEST_TEMPLATES));
})

/*
gulp.task('sass', () => {
	sass(SRC_SASS, {sourcemap: true, verbose: true})
	// options : https://github.com/sindresorhus/gulp-ruby-sass
		.on('error', sass.logError)
		.pipe(autoprefixer())
		// for inline sourcemaps
		// .pipe(sourcemaps.write())
		// for file sourcemaps
		.pipe(sourcemaps.write('maps', {
		    // includeContent: false,
		    // sourceRoot: SRC_SASS
		}))
		.pipe(gulp.dest(DEST_STYLES))
		.pipe(browserSync.reload({ stream:true }));
});
*/
gulp.task('sass', function () {
	let sassConfig = {};
	if (env === 'development') {
		sassConfig.sourceComments = 'map';
		sassConfig.errLogToConsole = true;
		sassConfig.outputStyle = 'expanded';
	} else if (env === 'production') {
		sassConfig.outputStyle = 'compressed';
	}

	let autoprefixerOptions = {
		browsers: ['last 2 versions', '> 5% in KR', 'not ie <= 8']
		// https://github.com/ai/browserslist#queries
	};

	return gulp.src(SRC_SASS)
		.pipe(sourcemaps.init())
		.pipe(sass(sassConfig).on('error', sass.logError))
		.pipe(autoprefixer(autoprefixerOptions))
		.pipe(sourcemaps.write())
		.pipe(gulp.dest(DEST_STYLES));
});

gulp.task('default', ['html', 'sass'], () => {
	browserSync.init(SRC_TO_WATCH, {
		server: {
			baseDir: DEST_BASE
		}
	});
	gulp.watch(SRC_SASS, ['sass']);
	gulp.watch(SRC_HTML, ['html']);
});

