//
//  ViewController.swift
//  SeeCloudSea
//
//  Created by 이현호 on 2023/06/25.
//

import UIKit

class ViewController: UIViewController {
    @IBOutlet var isCloudSeaLabel: UILabel!


    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func isCloudSeaButtonTapped(_ sender: Any) {
        self.getIsCloudSea()
    }
    
    
    
    func getIsCloudSea(){
        let urlString = "http://127.0.0.1:5000/model"
        guard let url = URL(string: urlString) else {
            DispatchQueue.main.async {
                self.showAlert(title: "url 설정 오류")
            }
            return
        }
        // URLRequest 생성
        var request = URLRequest(url: url)
 
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        
        let task = URLSession.shared.dataTask(with: request) { [weak self](data, response, error) in
            guard let self = self else {return}

            
            if let error = error{
                let code = (error as NSError).code
                DispatchQueue.main.async {
                    self.showAlert(title: "에러 발생")
                }
                switch code{
                case 17007: //아이디 및 비밀버호가 다를 때
                    return
                default:
                    return
                }
            }
            //httpResponse 응답 처리
            if let httpResponse = response as? HTTPURLResponse {
                if httpResponse.statusCode == 200 {
                    if let data = data {
                        let dataString = String(data: data, encoding: .utf8)
                        let numbersOnly = dataString?.filter { $0.isNumber }
                        let extractedNumber = Int(numbersOnly ?? "")

                        guard let isCloudSea = extractedNumber else {return}
                        
                        if isCloudSea == 1{
                            DispatchQueue.main.async {
                                self.isCloudSeaLabel.text = "운해 사냥 갑시다"
                            }
                        }else if isCloudSea == 0{
                            DispatchQueue.main.async {
                                self.isCloudSeaLabel.text = "내일은 쉽시다"
                            }
                        }else{
                            DispatchQueue.main.async {
                                self.showAlert(title: "데이터 오류")
                            }
                        }
                     
                    }
                } else {
                    DispatchQueue.main.async {
                        self.showAlert(title: "연결 실패")
                    }

                }
            }
        }
        task.resume()
        
    }
    
    func showAlert(title: String, message: String? = nil) {
           let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
           let okAction = UIAlertAction(title: "확인", style: .default, handler: nil)
           alertController.addAction(okAction)
           present(alertController, animated: true, completion: nil)
       }
    
}

