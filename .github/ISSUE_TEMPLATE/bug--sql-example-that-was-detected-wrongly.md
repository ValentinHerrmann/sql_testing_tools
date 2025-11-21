
name: 'Bug: SQL-Example that was detected wrongly'
about: Create a report to help us improve
title: 'Bug: SQL-Example'
labels: [bug]
assignees: ''


body:

The following aspects of the samples should be equal:
- type: checkbox
  attributes:
    label: Overall
- type: checkbox
  attributes:
    label: Columns
- type: checkbox
  attributes:
    label: Tables
- type: checkbox
  attributes:
    label: Condition
- type: checkbox
  attributes:
    label: Grouping
- type: checkbox
  attributes:
    label: Ordering

- type: textarea
  id: sqlA
  attributes:
    label: SQL Sample 1
    description: <<INSERT SQL QUERY SAMPLE 1>>
    render: sql
- type: textarea
  id: sqlB
  attributes:
    label: SQL Sample 2
    description: <<INSERT SQL QUERY SAMPLE 2>>
    render: sql
