#!/usr/bin/env python
# File generated by reverse AIRIUM translator (version 0.2.5).
# Any change will be overridden on next run.
# flake8: noqa E501 (line too long)

from airium import Airium

a = Airium()

with a.ul():
    a('<!-- L1 - DBs -->')
    with a.li(klass='level-1 db'):
        with a.div():
            a.a(href='#nrtcustomdb', _t='NRTCUSTOM.DB')
            a('<!-- L2 Objs (Table, Views, Procs etc)-->')
            with a.ul():
                with a.li(klass='obj table'):
                    with a.div():
                        a.a(href='#', _t='Tables')
                        a('<!-- L3 Sub Objects -->')
                        with a.ul():
                            with a.li(klass='obj table-table1'):
                                with a.div():
                                    a.a(href='#', _t='Table #1')
                            with a.li(klass='obj table-table2'):
                                with a.div():
                                    a.a(href='#', _t='Table #2')
                                    a.div(klass='warn', _t='Extra Info!')


if __name__ == '__main__':
    print(a)

