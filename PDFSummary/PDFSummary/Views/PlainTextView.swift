//
//  ContentView.swift
//  PDFSummary
//
//  Created by SeanHuang on 2025/3/17.
//

import SwiftUI

struct PlainTextView: View {
    @StateObject var vm: PlainTextViewModel = .init()
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
        }
        .padding()
    }
}

#Preview {
    PlainTextView()
}
