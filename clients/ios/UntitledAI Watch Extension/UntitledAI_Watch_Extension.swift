//
//  UntitledAI_Watch_Extension.swift
//  UntitledAI Watch Extension
//
//  Created by ethan on 1/31/24.
//
import WidgetKit
import SwiftUI

struct SimpleEntry: TimelineEntry {
    let date: Date
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date())
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        let entry = SimpleEntry(date: Date())
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        let entries = [SimpleEntry(date: Date())]
        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}

struct UntitledAI_Watch_ExtensionEntryView : View {
    var entry: SimpleEntry

    var body: some View {
        VStack {
            Text("U")
                .bold()
        }.padding()
    }
}

@main
struct UntitledAI_Watch_Extension: Widget {
    let kind: String = "UntitledAI_Watch_Extension"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            if #available(watchOS 10.0, *) {
                UntitledAI_Watch_ExtensionEntryView(entry: entry)
                    .containerBackground(.fill.tertiary, for: .widget)
            } else {
                UntitledAI_Watch_ExtensionEntryView(entry: entry)
                    .padding()
                    .background()
            }
        }
        .configurationDisplayName("UntitledAI")
        .description("UntitledAI")
    }
}
