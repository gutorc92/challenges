export default {
  methods: {
    stringLimit (string = '', maxLength = 10) {
      if (string.length && string.length > maxLength) {
        return string.substring(0, maxLength) + '...'
      } else {
        return string
      }
    },
    formatDate (date, final = ' 00:00:00 GMT') {
      let strDate = date.toDateString() + final
      strDate = strDate.substr(0, 3) + ',' + strDate.substr(2 + 1)
      strDate = strDate.substr(0, 3) + strDate.substr(2 + 1)
      strDate = strDate.substr(0, 5) + strDate.substr(9, 2) + strDate.substr(4, 4) + strDate.substr(11)
      return strDate
    },
    slugfy (text) {
      let slug = text.toLowerCase()
        .replace(/[àÀáÁâÂãäÄÅåª]+/g, 'a') // Special Characters #1
        .replace(/[èÈéÉêÊëË]+/g, 'e') // Special Characters #2
        .replace(/[ìÌíÍîÎïÏ]+/g, 'i') // Special Characters #3
        .replace(/[òÒóÓôÔõÕöÖº]+/g, 'o') // Special Characters #4
        .replace(/[ùÙúÚûÛüÜ]+/g, 'u') // Special Characters #5
        .replace(/[ýÝÿŸ]+/g, 'y') // Special Characters #6
        .replace(/[ñÑ]+/g, 'n') // Special Characters #7
        .replace(/[çÇ]+/g, 'c') // Special Characters #8
        .replace(/[ß]+/g, 'ss') // Special Characters #9
        .replace(/[Ææ]+/g, 'ae') // Special Characters #10
        .replace(/[Øøœ]+/g, 'oe') // Special Characters #11
        .replace(/[%]+/g, 'pct') // Special Characters #12
        .replace(/\s+/g, '-') // Replace spaces with -
        .replace(/[^\w\-]+/g, '') // eslint-disable-line
        .replace(/\-\-+/g, '-') // eslint-disable-line
        .replace(/^-+/, '') // Trim - from start of text
        .replace(/-+$/, '') // Trim - from end of text
      return slug
    }
  }
}
