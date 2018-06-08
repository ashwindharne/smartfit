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
    
    @IBOutlet var scrollView: UIScrollView!
    @IBOutlet var label: UILabel!
    
    @IBOutlet var i1: UIImageView!
    @IBOutlet var i2: UIImageView!
    @IBOutlet var i3: UIImageView!
    @IBOutlet var i4: UIImageView!
    @IBOutlet var i5: UIImageView!
    @IBOutlet var i6: UIImageView!
    @IBOutlet var i7: UIImageView!
    @IBOutlet var i8: UIImageView!
    @IBOutlet var i9: UIImageView!
    
    @IBOutlet var tag1: UILabel!
    @IBOutlet var tag2: UILabel!
    @IBOutlet var tag3: UILabel!
    @IBOutlet var tag4: UILabel!
    @IBOutlet var tag5: UILabel!
    @IBOutlet var tag6: UILabel!
    
    @IBOutlet var b1: UIButton!
    @IBOutlet var b2: UIButton!
    @IBOutlet var b3: UIButton!
    @IBOutlet var b4: UIButton!
    @IBOutlet var b5: UIButton!
    @IBOutlet var b6: UIButton!
    
    
    var labeltext = String()
    var tooBigb = Bool()
    var tooSmallb = Bool()
    var tooPriceyb = Bool()
    var wrongColorb = Bool()
    var showSimilarb = Bool()
    var current = 0
    var savedJSON = [String:NSDictionary]()
    var scriptUrl = String()
    var images: [UIImageView] = []
    var tags: [UILabel] = []
    var buttons: [UIButton] = []
    var itemNums: [String] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        images = [i1, i2, i3, i4, i5, i6, i7, i8, i9]
        tags = [tag1, tag2, tag3, tag4, tag5, tag6]
        buttons = [b1, b2, b3, b4, b5, b6]
        self.tag1.lineBreakMode = .byWordWrapping
        self.tag1.numberOfLines = 0
        view.addSubview(scrollView)
        let ref: FIRDatabaseReference!
        ref = FIRDatabase.database().reference()
        let surveyvc = SurveyViewController()
        
        //scriptUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/recommend/blahblah"
        let urlWithParams = scriptUrl + "?tooBig=\(tooBigb)&" + "tooSmall=\(tooSmallb)&" + "tooPricey=\(tooPriceyb)&" + "wrongColor=\(wrongColorb)&" + "showSimilar=\(showSimilarb)"
        print(urlWithParams)
        let myUrl = NSURL(string: urlWithParams);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
    
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
        
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! == "Error: Invalid item id") {
                let alert = UIAlertController(title: "This item does not exists", message: "Please scan again", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
            if (responseString! == "Error: Item cannot be both big and small"){
                let alert = UIAlertController(title: "Item cannot be both too big and too small", message: "Please scan again", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
            // Convert server json response to NSDictionary
            do {
                if let convertedJsonIntoDict = try JSONSerialization.jsonObject(with: data!, options: []) as? [String: NSDictionary] {
                    let length = convertedJsonIntoDict.count
                    // Print out dictionary
                    //print(convertedJsonIntoDict)
                    //let value = convertedJsonIntoDict["221025"]!
                    var counter = 0;
                    for (key, value) in convertedJsonIntoDict{
                        
                        //print(value)
                        let brand = value["brand"]! as! String
                        let price = value["price"]! as! String
                        let size = String(describing: value["size"]!)
                        //self.size = value["size"]
                        print(value["size"]!)
                        print(type(of: value["size"]))
                        
                        self.itemNums.append(key)
                        
                        let pic = value["image"]!
                        let imageUrlString = pic
                        let imageUrl:URL = URL(string: imageUrlString as! String)!

                        // Start background thread so that image loading does not make app unresponsive
                        DispatchQueue.global(qos: .userInitiated).async {
                            
                            //self.setLabels(brand: self.brand, price: self.price)
                            let imageData:NSData = NSData(contentsOf: imageUrl)!

                            // When from background thread, UI needs to be updated on main_queue
                            DispatchQueue.main.async {
                                let image = UIImage(data: imageData as Data)
                                self.images[counter].image = image
                                let heart = UIImage(named: "open-heart.png") as UIImage?
                                self.buttons[counter].setImage(heart, for: .normal)
                                
                                self.tags[counter].text = brand + "\nsize: " + size + "\n$" + price
                                if (counter < 5){
                                    counter += 1
                                }
                                
                            }
                        }
                    }
                  
                    
                }
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
        
        
        
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    @IBAction func B1(_ sender: Any) {
        let heart = UIImage(named: "closed-heart.png") as UIImage?
        b1.setImage(heart, for: .normal)
        let fitUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/fitting/request_item?roomNumber=1&itemID=" + itemNums[0]
        print(fitUrl)
        let myUrl = NSURL(string: fitUrl);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
            
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! as String == "Error: " + self.itemNums[0] + " has already been requested!" ){
                let alert = UIAlertController(title: "Item has already been requested", message: "", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            // Convert server json response to NSDictionary
            do {
                
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
    }
    @IBAction func B2(_ sender: Any) {
        let heart = UIImage(named: "closed-heart.png") as UIImage?
        b2.setImage(heart, for: .normal)
        let fitUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/fitting/request_item?roomNumber=1&itemID=" + itemNums[1]
        let myUrl = NSURL(string: fitUrl);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
            
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! as String == "Error: " + self.itemNums[1] + " has already been requested!" ){
                let alert = UIAlertController(title: "Item has already been requested", message: "", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
            // Convert server json response to NSDictionary
            do {
                
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
    }
    @IBAction func B3(_ sender: Any) {
        let heart = UIImage(named: "closed-heart.png") as UIImage?
        b3.setImage(heart, for: .normal)
        
        let fitUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/fitting/request_item?roomNumber=1&itemID=" + itemNums[2]
        let myUrl = NSURL(string: fitUrl);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
            
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! as String == "Error: " + self.itemNums[2] + " has already been requested!" ){
                let alert = UIAlertController(title: "Item has already been requested", message: "", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
            // Convert server json response to NSDictionary
            do {
                
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
    }
    @IBAction func B4(_ sender: Any) {
        let heart = UIImage(named: "closed-heart.png") as UIImage?
        b4.setImage(heart, for: .normal)
        
        let fitUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/fitting/request_item?roomNumber=1&itemID=" + itemNums[3]
        let myUrl = NSURL(string: fitUrl);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
            
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! as String == "Error: " + self.itemNums[3] + " has already been requested!" ){
                let alert = UIAlertController(title: "Item has already been requested", message: "", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
            // Convert server json response to NSDictionary
            do {
                
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
    }
    @IBAction func B5(_ sender: Any) {
        let heart = UIImage(named: "closed-heart.png") as UIImage?
        b5.setImage(heart, for: .normal)
        
        let fitUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/fitting/request_item?roomNumber=1&itemID=" + itemNums[4]
        let myUrl = NSURL(string: fitUrl);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
            
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! as String == "Error: " + self.itemNums[4] + " has already been requested!" ){
                let alert = UIAlertController(title: "Item has already been requested", message: "", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            // Convert server json response to NSDictionary
            do {
                
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
    }
    @IBAction func B6(_ sender: Any) {
        let heart = UIImage(named: "closed-heart.png") as UIImage?
        b6.setImage(heart, for: .normal)
        
        let fitUrl = "http://ec2-52-53-219-19.us-west-1.compute.amazonaws.com/fitting/request_item?roomNumber=1&itemID=" + itemNums[5]
        let myUrl = NSURL(string: fitUrl);
        let request = NSMutableURLRequest(url:myUrl! as URL);
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            // Check for error
            if error != nil
            {
                print("error=\(error)")
                return
            }
            
            // Print out response string
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("responseString = \(responseString)")
            
            if (responseString! as String == "Error: " + self.itemNums[5] + " has already been requested!" ){
                let alert = UIAlertController(title: "Item has already been requested", message: "", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
            // Convert server json response to NSDictionary
            do {
                
            } catch let error as NSError {
                print(error.localizedDescription)
            }
            
        }
        
        task.resume()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillLayoutSubviews(){
        super.viewWillLayoutSubviews()
        scrollView.contentSize = CGSize(width: 375, height: 1200)
    }
    
    
}

