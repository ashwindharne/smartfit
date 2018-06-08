//
//  ViewController.swift
//  SmartFit
//
//  Created by SIMRAN KASHYAP on 5/2/18.
//  Copyright © 2018 SIMRAN KASHYAP. All rights reserved.
//

import UIKit
import Firebase
import FirebaseDatabase


class SurveyViewController: UIViewController {
    
    
    @IBOutlet var tooBig: UIButton!
    @IBOutlet var tooSmall: UIButton!
    @IBOutlet var tooPricey: UIButton!
    @IBOutlet var wrongColor: UIButton!
    @IBOutlet var showSimilar: UIButton!
    
    var tooBigb:Bool = false
    var tooSmallb = false
    var tooPriceyb = false
    var wrongColorb = false
    var showSimilarb = false
    var scriptUrl = String()
    
    @IBAction func buttonClicked(_ sender: UIButton)
    {
        let button = sender as UIButton
        var image: UIImage
        if(button == tooBig)
        {
            image = UIImage(named: "tooBig" + (tooBigb == true ? "I" : "A") + ".png")!
            button.setImage(image, for: .normal)
            tooBigb = !tooBigb
        }
        else if(button == tooSmall)
        {
            image = UIImage(named: "tooSmall" + (tooSmallb ? "I": "A") + ".png")!
            button.setImage(image, for: .normal)
            tooSmallb = !tooSmallb
        }
        else if(button == tooPricey)
        {
            image = UIImage(named: "tooPricey" + (tooPriceyb ? "I": "A") + ".png")!
            button.setImage(image, for: .normal)
            tooPriceyb = !tooPriceyb
        }
        else if(button == wrongColor)
        {
            image = UIImage(named: "wrongColor" + (wrongColorb ? "I": "A") + ".png")!
            button.setImage(image, for: .normal)
            wrongColorb = !wrongColorb
        }
        else if(button == showSimilar)
        {
            image = UIImage(named: "showSimilar" + (showSimilarb ? "I": "A") + ".png")!
            button.setImage(image, for: .normal)
            showSimilarb = !showSimilarb
        }
        
    }
    
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let ref: FIRDatabaseReference!
        ref = FIRDatabase.database().reference()
        // Do any additional setup after loading the view, typically from a nib.]
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?)
    {
        var DestViewController : SuggestionViewController = segue.destination as! SuggestionViewController
        DestViewController.tooBigb = tooBigb
        DestViewController.tooSmallb = tooSmallb
        DestViewController.tooPriceyb = tooPriceyb
        DestViewController.wrongColorb = wrongColorb
        DestViewController.showSimilarb = showSimilarb
        DestViewController.scriptUrl = scriptUrl
    }


}

