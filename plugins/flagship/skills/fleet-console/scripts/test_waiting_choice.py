import unittest
import fleet_sessions as fleet

class WaitingChoiceTests(unittest.TestCase):
    def packet(self, **changes):
        p = dict(provider='claude', session_id='00000000-0000-4000-8000-000000000002',
                 cli_version='2.1.285', kind='interactive', state='waiting',
                 waiting_tool='AskUserQuestion', identity_verified=True,
                 original_scope_reviewed=True, explicit_user_decision=True,
                 supported_controls_reviewed=True, observed_at=fleet.now().isoformat(),
                 choices=['Keep current model', 'Try previous model'],
                 selected_label='Keep current model', custom_base_url=True)
        p.update(changes); return p

    def test_queued_success_cannot_resolve_interactive_choice(self):
        p=self.packet(peer_receipt={'success':True,'msg_id':'fixture','status':'queued'})
        r=fleet.waiting_choice_route(p)
        self.assertEqual(r['route'],'original_prompt_input')
        self.assertFalse(r['prompt_answered'])
        self.assertIn('custom endpoint',r['remote_control'])

    def test_agent_view_applies_only_to_verified_background_row(self):
        for kind,expected in [('interactive','original_prompt_input'),('background','background_agent_view')]:
            with self.subTest(kind=kind):
                self.assertEqual(fleet.waiting_choice_route(self.packet(kind=kind,agent_view_peek_available=True))['route'],expected)

    def test_sdk_callback_requires_ownership_of_same_query(self):
        for owner,expected in [(False,'original_prompt_input'),(True,'own_sdk_callback')]:
            with self.subTest(owner=owner):
                r=fleet.waiting_choice_route(self.packet(kind='sdk',owns_sdk_query=owner))
                self.assertEqual(r['route'],expected); self.assertFalse(r['prompt_answered'])

    def test_permission_unknown_identity_and_unsettled_decision_refused(self):
        for change in [dict(waiting_tool='Bash'),dict(state='idle'),dict(kind='unknown'),
                       dict(identity_verified=False),dict(explicit_user_decision=False),dict(session_id='short')]:
            with self.subTest(change=change),self.assertRaises(ValueError):
                fleet.waiting_choice_route(self.packet(**change))

    def test_stale_or_changed_prompt_cannot_reuse_prior_selection(self):
        for change in [dict(observed_at='2000-01-01T00:00:00Z'),dict(selected_label='invented answer'),
                       dict(choices=['Keep current model','Keep current model'])]:
            with self.subTest(change=change),self.assertRaises(ValueError):
                fleet.waiting_choice_route(self.packet(**change))

    def test_unreviewed_future_controls_require_reverification(self):
        r=fleet.waiting_choice_route(self.packet(cli_version='future-version',supported_controls_reviewed=False))
        self.assertEqual(r['route'],'recheck_current_supported_controls')
        self.assertFalse(r['prompt_answered'])

if __name__=='__main__':unittest.main()
