module.exports = {
    future: {
        removeDeprecatedGapUtilities: true,
        purgeLayersByDefault: true,
    },
    content: {
        enabled: true, //true for production build
        content: [
            '../**/templates/*.html',
            '../**/templates/**/*.html'
        ]
    },
    theme: {
        extend: {},
    },
    variants: {},
    plugins: [],
  }
  //tailwindcss  build -i ./static/css/tailwind.css -o ./static/css/style.css && cleancss -o ./static/css/style.min.css ./static/css/style.css
