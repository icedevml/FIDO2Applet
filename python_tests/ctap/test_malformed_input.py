import secrets

from fido2.ctap import CtapError

from .ctap_test import CTAPTestCase


class CTAPMalformedInputTestCase(CTAPTestCase):

    def test_notices_invalid_keyparams_later_in_array(self):
        self.basic_makecred_params['key_params'].append({})
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.MISSING_PARAMETER, e.exception.code)

    def test_options_not_a_map(self):
        self.basic_makecred_params['options'] = []
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_extensions_not_a_map(self):
        self.basic_makecred_params['extensions'] = "Good and Loud"
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_too_many_extensions(self):
        d = {}
        for x in range(30):
            d[str(x)] = True
        self.basic_makecred_params['extensions'] = d
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_rp_icon_not_text(self):
        self.basic_makecred_params['rp']['icon'] = 454
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_user_icon_not_text(self):
        self.basic_makecred_params['user']['icon'] = 454
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_bogus_makecred_options(self):
        self.basic_makecred_params['options'] = {'frobble': 23}
        self.ctap2.make_credential(**self.basic_makecred_params)

    def test_bogus_getassert_options(self):
        cred = self.ctap2.make_credential(**self.basic_makecred_params)
        self.get_assertion_from_cred(cred, options={'bogus': 123})

    def test_bogus_exclude_list(self):
        self.basic_makecred_params['exclude_list'] = 12345

        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)

        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_bogus_exclude_list_entry(self):
        self.basic_makecred_params['exclude_list'] = [12345]

        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)

        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_bogus_exclude_list_entry_after_valid(self):
        cred = self.ctap2.make_credential(**self.basic_makecred_params)

        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params, exclude_list=[
                self.get_descriptor_from_ll_cred(cred),
                12334
            ])

        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_user_icon_not_text(self):
        self.basic_makecred_params['user']['icon'] = secrets.token_bytes(16)

        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)

        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_rp_icon_not_text(self):
        self.basic_makecred_params['rp']['icon'] = secrets.token_bytes(16)

        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)

        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_rejects_non_string_type_in_array(self):
        self.basic_makecred_params['key_params'].append({
            "type": 3949,
            "alg": 12
        })
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_rejects_es256_with_non_string_type(self):
        self.basic_makecred_params['key_params'].append({
            "type": False,
            "alg": -7
        })
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_rejects_non_integer_alg_in_array(self):
        self.basic_makecred_params['key_params'].append({
            "type": "public-key",
            "alg": "foo"
        })
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)

    def test_rejects_non_integer_alg_at_start_of_array(self):
        self.basic_makecred_params['key_params'].insert(0, {
            "type": "public-key",
            "alg": "foo"
        })
        with self.assertRaises(CtapError) as e:
            self.ctap2.make_credential(**self.basic_makecred_params)
        self.assertEqual(CtapError.ERR.CBOR_UNEXPECTED_TYPE, e.exception.code)
