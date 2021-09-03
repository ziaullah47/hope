# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_household_0_with_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTowZmRiZjJmYy1lOTRlLTRjNjQtYWNjZS02ZTdlZGQ0YmJkODc=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                },
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZToxMjM5OGM3MS04MWVmLTRlMjQtOTY0ZC1mNzdlODUzOTcxYWI=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': None
                        }
                    }
                },
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTpjOThkMDM3My0xYjIwLTQ4ZWItOGI4Ny03MjM3NDc3ZWQ3ODI=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                }
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_household_1_without_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_individual_0_with_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTowZmRiZjJmYy1lOTRlLTRjNjQtYWNjZS02ZTdlZGQ0YmJkODc=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                },
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZToxMjM5OGM3MS04MWVmLTRlMjQtOTY0ZC1mNzdlODUzOTcxYWI=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': None
                        }
                    }
                },
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTpjOThkMDM3My0xYjIwLTQ4ZWItOGI4Ny03MjM3NDc3ZWQ3ODI=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                }
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_individual_1_without_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_payment_record_0_with_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTowZmRiZjJmYy1lOTRlLTRjNjQtYWNjZS02ZTdlZGQ0YmJkODc=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                }
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_payment_record_1_without_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_two_payment_records_0_with_permission 1'] = {
    'data': {
        'existingGrievanceTickets': {
            'edges': [
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTowZmRiZjJmYy1lOTRlLTRjNjQtYWNjZS02ZTdlZGQ0YmJkODc=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                },
                {
                    'node': {
                        'category': 3,
                        'id': 'R3JpZXZhbmNlVGlja2V0Tm9kZTpjOThkMDM3My0xYjIwLTQ4ZWItOGI4Ny03MjM3NDc3ZWQ3ODI=',
                        'issueType': 1,
                        'sensitiveTicketDetails': {
                            'household': {
                                'size': 1
                            },
                            'individual': {
                                'fullName': 'John Doe'
                            },
                            'paymentRecord': {
                                'fullName': 'John Doe'
                            }
                        }
                    }
                }
            ]
        }
    }
}

snapshots['TestAlreadyExistingFilterTickets::test_filter_existing_tickets_by_two_payment_records_1_without_permission 1'] = {
    'data': {
        'existingGrievanceTickets': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 10
                }
            ],
            'message': 'Permission Denied',
            'path': [
                'existingGrievanceTickets'
            ]
        }
    ]
}