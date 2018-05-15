//
//  SuggestionViewController.swift
//  SmartFit
//
//  Created by SIMRAN KASHYAP on 5/9/18.
//  Copyright © 2018 SIMRAN KASHYAP. All rights reserved.
//

import UIKit
import Firebase
import FirebaseDatabase


class SuggestionViewController: UIViewController {
    
    @IBOutlet var label: UILabel!
    
    var labeltext = String()
    var tooBigb = Bool()
    var tooSmallb = Bool()
    var tooPriceyb = Bool()
    var wrongColorb = Bool()
    var showSimilarb = Bool()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let ref: FIRDatabaseReference!
        ref = FIRDatabase.database().reference()
        let surveyvc = SurveyViewController()
        
        labeltext = "Query items that are " + (tooBigb ? "smaller in size " : "") + (tooSmallb ? "larger in size " : "") + (tooPriceyb ? "cheaper " : "") + (wrongColorb ? "different colors " : "") + (showSimilarb ? "similar in terms of attribute values" : "") + "."
        self.label.text = labeltext
        
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

}
