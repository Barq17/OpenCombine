//
//  CustomSubscription.swift
//  
//
//  Created by Sergej Jaskiewicz on 16.06.2019.
//

#if OPENCOMBINE_COMPATIBILITY_TEST
import Combine
#else
import OpenCombine
#endif

@available(macOS 10.15, *)
final class CustomSubscription: Subscription {

    enum Event: Equatable {
        case requested(Subscribers.Demand)
        case canceled
    }

    private(set) var history: [Event] = []

    var lastRequested: Subscribers.Demand? {
        history.lazy.compactMap {
            switch $0 {
            case .requested(let demand):
                return demand
            case .canceled:
                return nil
            }
        }.last
    }

    var canceled = false

    func request(_ demand: Subscribers.Demand) {
        history.append(.requested(demand))
    }

    func cancel() {
        history.append(.canceled)
        canceled = true
    }
}