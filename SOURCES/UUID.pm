# Compatibility wrapper to emulate UUID::generate()
# using UUID::Tiny

package UUID;

use strict;
use UUID::Tiny ':std';

sub generate {
    my $ref = \shift;
    ${$ref} = UUID::Tiny::create_uuid();
}

sub unparse {
    my $uuid_ref = \shift;
    my $result_ref = \shift;
    ${$result_ref} = UUID::Tiny::UUID_to_string(${$uuid_ref});
}

1;
