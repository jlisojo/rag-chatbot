# Simple Events CPT & Pro — Internal Reference Doc

This is sample content used to demonstrate the RAG chatbot. Replace the files in
`data/sample_docs/` with your own PDFs, Markdown, or text files, then run the
ingest step again.

## Simple Events CPT (Free Core)

Simple Events CPT is a WordPress plugin that registers a custom post type called
`se_event`. It stores event metadata such as start date, end date, start time,
end time, venue, address, pricing, and a registration link. It ships with
theme-overridable archive and single templates, Schema.org JSON-LD markup for
search engines, a `[simple_events]` shortcode, and a native Gutenberg "Event
Grid" block with live preview and sidebar controls for title, event count, and
button text.

## Simple Events Pro (Premium Add-on)

Simple Events Pro is a separate plugin that depends on Simple Events CPT. It
adds a recurrence engine built on PHP's DateTimeImmutable, supporting daily,
weekly, and monthly repeating events with configurable intervals and end
dates. It also supports per-occurrence exceptions, so a single date in a
recurring series can be skipped or rescheduled without breaking the pattern.

Simple Events Pro also includes an AJAX-powered monthly calendar view,
available both as a `[simple_events_calendar]` shortcode and as a native
Gutenberg "Event Calendar" block. For calendar subscriptions, it generates
RFC 5545 compliant iCalendar (.ics) files for both individual event downloads
and a live subscription feed compatible with Google Calendar, Outlook, and
Apple Calendar.

## Deployment Notes

Both plugins are pure PHP and JavaScript with no external API dependencies.
Simple Events CPT is currently under review for the official WordPress.org
Plugin Directory. Both plugins are open source and hosted on GitHub under the
`jlisojo` account.
