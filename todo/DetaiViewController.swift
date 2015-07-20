//
//  DetaiViewController.swift
//  todo
//
//  Created by 钟信 on 15/7/19.
//  Copyright (c) 2015年 zhongxin. All rights reserved.
//

import UIKit

class DetaiViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var childButton: UIButton!
    @IBOutlet weak var phoneButton: UIButton!
    @IBOutlet weak var shoppingCartButton: UIButton!
    @IBOutlet weak var travelButton: UIButton!
    @IBOutlet weak var todoItem: UITextField!
    @IBOutlet weak var todoDate: UIDatePicker!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        todoItem.delegate = self

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func resetButtons() {
        childButton.selected = false
        phoneButton.selected = false
        shoppingCartButton.selected = false
        travelButton.selected = false
    }
    @IBAction func childTapped(sender: AnyObject) {
        resetButtons()
        childButton.selected = true
        
    }
    
    @IBAction func phoneTapped(sender: AnyObject) {
        resetButtons()
        phoneButton.selected = true
    }
    @IBAction func shoppingCartButton(sender: AnyObject) {
        resetButtons()
        shoppingCartButton.selected = true
    }
    @IBAction func travelTapped(sender: AnyObject) {
        resetButtons()
        travelButton.selected = true
    }
    @IBAction func okTapped(sender: AnyObject) {
        var image = ""
        if childButton.selected {
            image = "child-selected"
        }
        else if phoneButton.selected {
            image = "phone-selected"
        }
        else if shoppingCartButton .selected {
            image = "shopping-cart-selected"
        }
        else if travelButton.selected {
            image = "travel-selected"
        }
        let uuid = NSUUID().UUIDString
        var todo = TodoModel(id: uuid, image: image, title: todoItem.text, date: todoDate.date)
        todos.append(todo)

    }
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    override func touchesEnded(touches: Set<NSObject>, withEvent event: UIEvent) {
        todoItem.resignFirstResponder()
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
