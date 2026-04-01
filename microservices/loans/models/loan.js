const mongoose = require('mongoose') 


const loanSchema = new mongoose.Schema({
  book_id: {
    type: Number,
    required: true
  },
  user_id: {
    type: Number,
    required: true
  },
  loan_date: {
    type: Date,
    default: Date.now
  },
  return_date: {
    type: Date
  },
  status: {
    type: String,
    enum: ['active', 'returned'],
    default: 'active'
  }
});

module.exports = mongoose.model('Loan', loanSchema);