# Compatibility wrapper to emulate UUID::generate()
# using UUID::Tiny

package UUID;

use strict;
use UUID::Tiny ':std';

sub generate {
    my $ref = \shift;
    ${$ref} = UUID::Tiny::create_uuid();
}

1;
