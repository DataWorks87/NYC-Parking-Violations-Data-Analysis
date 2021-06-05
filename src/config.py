mappings = {
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": { 
      "plate": { "type": "text" },
      "state": { "type": "text" },
      "license_type": { "type": "text" },
      
      "violation": { "type": "text" },
      "judgement_entry_date": { "type": "date" },
      "precinct": { "type": "text" },
      "county": { "type": "text" },
      "issuing_agency": { "type": "text" },
      "violation_status": { "type": "text" },
      "summons_image": {
          "properties":{
              "url":{"type":"string"}},
      "description":{"type":"text"},
      
      "issue_date": { "type": "date", "format":"yyyy-MM-dd" },
      "violation_time": { "type": "date" },
      
      "summons_number": { "type": "float" },
      "fine_amount": { "type": "float" },
      "penalty_amount": { "type": "float" },
      "interest_amount": { "type": "float" },
      "reduction_amount": { "type": "float" },
      "payment_amount": { "type": "float" },
      "amount_due": { "type": "float" },
      }
    }
  }
}